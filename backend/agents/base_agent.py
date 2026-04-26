"""
BaseAgent — shared interface for all four domain agents.
Each agent fetches live data, calls Claude Sonnet, emits structured JSON,
and pushes an alert to the shared AlertPriorityQueue.
"""
import asyncio
import json
from datetime import datetime, timezone
from typing import Any

import anthropic

from config import settings
from utils.priority_queue import AlertPriorityQueue

_anthropic = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

# Shared queue — all agents push here, orchestrator pops
alert_queue = AlertPriorityQueue()

# Agent state registry — keyed by domain, read by frontend via WebSocket
agent_states: dict[str, dict] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class BaseAgent:
    domain: str = "base"
    poll_interval: int = 60  # seconds between fetch→analyze cycles
    _system_prompt: str = "You are an infrastructure monitoring AI agent."

    def __init__(self, broadcast_fn):
        """broadcast_fn is manager.broadcast from routers/ws.py."""
        self._broadcast = broadcast_fn
        agent_states[self.domain] = {
            "domain": self.domain,
            "status": "idle",
            "last_signal": None,
            "last_reasoning": None,
            "confidence": None,
            "last_updated": None,
        }

    async def fetch_data(self) -> dict[str, Any]:
        raise NotImplementedError

    async def analyze(self, data: dict[str, Any]) -> dict[str, Any]:
        """Send data summary to Claude Sonnet, return structured reasoning JSON."""
        prompt = (
            f"Current infrastructure data for the {self.domain} domain in NYC:\n"
            f"{json.dumps(data, indent=2, default=str)}\n\n"
            "Return ONLY valid JSON matching this schema — no prose, no markdown:\n"
            '{\n'
            '  "domain": "<domain>",\n'
            '  "severity": <0.0-10.0>,\n'
            '  "signal": "<1-sentence finding>",\n'
            '  "affected_nodes": ["<node_id>"],\n'
            '  "reasoning": "<2-3 sentences>",\n'
            '  "recommended_action": "<1 sentence>",\n'
            '  "confidence": <0.0-1.0>\n'
            '}'
        )
        message = _anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=512,
            system=self._system_prompt,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        # Strip markdown fences if Claude wraps it
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)

    async def emit_alert(self, analysis: dict[str, Any]) -> None:
        severity = float(analysis.get("severity", 5.0))
        alert = {
            **analysis,
            "id": f"{self.domain}-{_now_iso()}",
            "timestamp": _now_iso(),
        }
        alert_queue.push(alert, priority=severity)

        # Update public agent state
        agent_states[self.domain].update({
            "status": "alert" if severity >= 7 else "analyzing",
            "last_signal": analysis.get("signal"),
            "last_reasoning": analysis.get("reasoning"),
            "confidence": analysis.get("confidence"),
            "last_updated": _now_iso(),
        })

        await self._broadcast({"type": "alert", "payload": alert})
        await self._broadcast({
            "type": "agent_update",
            "payload": agent_states[self.domain],
        })
        await self._broadcast({
            "type": "queue_snapshot",
            "payload": alert_queue.to_list()[:10],
        })

    async def run(self) -> None:
        """Continuous polling loop — call this as an asyncio task."""
        agent_states[self.domain]["status"] = "analyzing"
        await self._broadcast({
            "type": "agent_update",
            "payload": agent_states[self.domain],
        })
        while True:
            try:
                data = await self.fetch_data()
                analysis = await self.analyze(data)
                await self.emit_alert(analysis)
            except Exception as exc:
                agent_states[self.domain]["status"] = "idle"
                # Broadcast a low-severity synthetic alert so UI stays alive
                await self._broadcast({
                    "type": "agent_update",
                    "payload": {
                        **agent_states[self.domain],
                        "last_signal": f"Data fetch error: {exc}",
                        "last_updated": _now_iso(),
                    },
                })
            await asyncio.sleep(self.poll_interval)
