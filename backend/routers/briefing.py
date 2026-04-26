"""
City briefing generation for current cascade state.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any

import anthropic
from fastapi import APIRouter

from agents.base_agent import agent_states, alert_queue
from config import settings
from graph.dijkstra_reroute import get_last_reroute
from graph.infrastructure_graph import graph
from routers.simulation import _node_status

router = APIRouter(prefix="/briefing", tags=["briefing"])
_anthropic = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _severity(statuses: list[str], alerts: list[dict]) -> str:
    if "failed" in statuses or "critical" in statuses:
        return "CRITICAL"
    if any(float(alert.get("severity", 0)) >= 7 for alert in alerts):
        return "HIGH"
    if statuses or alerts:
        return "MEDIUM"
    return "LOW"


def _affected_systems() -> list[dict[str, Any]]:
    systems = []
    for node_id, status in _node_status.items():
        node = graph.G.nodes[node_id] if node_id in graph.G else {}
        systems.append({
            "node_id": node_id,
            "name": node.get("name", node_id),
            "domain": node.get("type", "unknown"),
            "status": status,
        })
    return systems


def _cascade_origin() -> dict[str, Any] | None:
    failed = [node_id for node_id, status in _node_status.items() if status == "failed"]
    if not failed:
        return None
    node_id = failed[0]
    node = graph.G.nodes[node_id] if node_id in graph.G else {}
    return {
        "node_id": node_id,
        "name": node.get("name", node_id),
        "domain": node.get("type", "unknown"),
    }


def _fallback_briefing(context: dict[str, Any]) -> dict[str, Any]:
    generated_at = _now()
    severity = context["severity"]
    origin = context.get("cascade_origin")
    affected = context["affected_systems"]
    rerouting = context.get("rerouting")
    origin_text = origin["name"] if origin else "the current monitored incident"
    systems_text = ", ".join(sorted({item["domain"] for item in affected})) or "no confirmed systems"
    actions = [
        "Maintain unified command across transit, water, health, and emergency operations.",
        "Prioritize field validation of failed and critical nodes before reopening dependent service.",
        "Use the active reroute recommendation for emergency movement until corridor status is cleared.",
    ]
    if not rerouting:
        actions[-1] = "Continue monitoring for reroute requirements as additional cascade nodes arrive."
    summary = (
        f"{origin_text} has produced a {severity.lower()} cascade posture across {systems_text}. "
        f"{len(affected)} infrastructure nodes currently require operational attention."
    )
    full_report = (
        f"{summary}\n\n"
        f"Recommended actions: {' '.join(actions)}"
    )
    return {
        "incident_id": generated_at.strftime("CASCADE-%Y%m%d-%H%M"),
        "generated_at": generated_at.isoformat(),
        "severity": severity,
        "summary": summary,
        "affected_systems": affected,
        "cascade_origin": origin,
        "predicted_peak_impact": context["predicted_peak_impact"],
        "recommended_actions": actions,
        "rerouting": rerouting,
        "full_report": full_report,
    }


def _parse_json_response(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1] if len(parts) > 1 else text
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


@router.post("/generate")
async def generate_briefing() -> dict[str, Any]:
    alerts = alert_queue.to_list()[:10]
    affected = _affected_systems()
    statuses = [item["status"] for item in affected]
    severity = _severity(statuses, alerts)
    generated_at = _now()
    predicted_peak = generated_at + timedelta(minutes=30 if severity == "CRITICAL" else 15)
    context = {
        "incident_id": generated_at.strftime("CASCADE-%Y%m%d-%H%M"),
        "generated_at": generated_at.isoformat(),
        "severity": severity,
        "affected_systems": affected,
        "cascade_origin": _cascade_origin(),
        "predicted_peak_impact": predicted_peak.isoformat(),
        "active_alerts": alerts,
        "agent_states": agent_states,
        "rerouting": get_last_reroute(),
    }
    prompt = (
        "Using the live CascadeOS telemetry below, return ONLY valid JSON matching this schema:\n"
        "{\n"
        '  "incident_id": "CASCADE-YYYYMMDD-HHmm",\n'
        '  "generated_at": "ISO timestamp",\n'
        '  "severity": "LOW|MEDIUM|HIGH|CRITICAL",\n'
        '  "summary": "2 sentence executive summary",\n'
        '  "affected_systems": [{"node_id": "...", "status": "...", "domain": "..."}],\n'
        '  "cascade_origin": {"node_id": "...", "name": "..."},\n'
        '  "predicted_peak_impact": "ISO timestamp",\n'
        '  "recommended_actions": ["action 1", "action 2"],\n'
        '  "rerouting": null,\n'
        '  "full_report": "full plain English report"\n'
        "}\n\n"
        "Preserve the incident_id, generated_at, affected_systems, cascade_origin, "
        "predicted_peak_impact, and rerouting values from the telemetry when present.\n"
        f"{json.dumps(context, indent=2, default=str)}"
    )
    try:
        message = _anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1400,
            system=(
                "You are the Emergency Operations Director for New York City. "
                "Generate a structured incident briefing for city officials and "
                "emergency responders. Be concise, factual, and actionable."
            ),
            messages=[{"role": "user", "content": prompt}],
        )
        briefing = _parse_json_response(message.content[0].text)
        if context["rerouting"] and not briefing.get("rerouting"):
            briefing["rerouting"] = context["rerouting"]
        return {
            **_fallback_briefing(context),
            **briefing,
        }
    except Exception:
        return _fallback_briefing(context)
