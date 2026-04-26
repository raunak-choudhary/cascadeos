"""
Coordinator agent — pops from the shared AlertPriorityQueue,
decides if multiple domain alerts constitute a cascade event,
and triggers cascade BFS when 2+ domains are affected within 15 minutes.
Runs as an asyncio background task.
"""
import asyncio
from collections import defaultdict
from datetime import datetime, timezone, timedelta

from agents.base_agent import alert_queue, agent_states, _now_iso
from data.sliding_window_311 import SlidingWindow311
from data.nyc_open_data import fetch_311_complaints

CASCADE_WINDOW_MINUTES = 15
CASCADE_DOMAIN_THRESHOLD = 2  # 2+ domains affected triggers cascade check

_window_311 = SlidingWindow311(window_seconds=600, surge_threshold=8)

# Track recent high-severity alerts by domain
_recent_alerts: dict[str, list[dict]] = defaultdict(list)


def _prune_stale(now: datetime):
    cutoff = now - timedelta(minutes=CASCADE_WINDOW_MINUTES)
    for domain in list(_recent_alerts.keys()):
        _recent_alerts[domain] = [
            a for a in _recent_alerts[domain]
            if datetime.fromisoformat(a["timestamp"]) > cutoff
        ]


async def run_orchestrator(broadcast_fn) -> None:
    """Background loop — pop alerts, check for cascade, run 311 window."""
    poll_311_counter = 0

    while True:
        now = datetime.now(timezone.utc)
        _prune_stale(now)

        # --- Pop and process alerts from queue ---
        while alert_queue.size() > 0:
            alert = alert_queue.pop()
            if not alert:
                break
            domain = alert.get("domain", "unknown")
            severity = float(alert.get("severity", 0))

            if severity >= 5.0:
                _recent_alerts[domain].append({
                    "timestamp": alert.get("timestamp", _now_iso()),
                    "severity": severity,
                    "signal": alert.get("signal", ""),
                    "affected_nodes": alert.get("affected_nodes", []),
                })

            # Broadcast processed alert back to queue snapshot
            await broadcast_fn({
                "type": "queue_snapshot",
                "payload": alert_queue.to_list()[:10],
            })

            # Check cascade condition
            active_domains = [d for d, alerts in _recent_alerts.items() if alerts]
            if len(active_domains) >= CASCADE_DOMAIN_THRESHOLD:
                origin_nodes = []
                for d in active_domains:
                    for a in _recent_alerts[d]:
                        origin_nodes.extend(a.get("affected_nodes", []))

                if origin_nodes:
                    await broadcast_fn({
                        "type": "cascade_start",
                        "payload": {
                            "domains_affected": active_domains,
                            "origin_nodes": list(set(origin_nodes)),
                            "triggered_at": _now_iso(),
                            "message": (
                                f"Multi-domain cascade detected across: "
                                f"{', '.join(active_domains)}. "
                                f"Initiating cascade BFS from affected nodes."
                            ),
                        },
                    })

        # --- 311 sliding window check every 5 cycles (5 × 3s = 15s) ---
        poll_311_counter += 1
        if poll_311_counter >= 5:
            poll_311_counter = 0
            try:
                complaints = await fetch_311_complaints(limit=50)
                _window_311.ingest(complaints)
                surges = _window_311.detect_surges()
                for surge in surges:
                    await broadcast_fn({"type": "311_surge", "payload": surge})
            except Exception:
                pass

        await asyncio.sleep(3)
