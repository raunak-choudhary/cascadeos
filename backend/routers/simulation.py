"""
Simulation router — triggers cascade BFS, streams results over WebSocket,
resets node state, and exposes preset demo scenarios.
"""
import asyncio
from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from config import settings
from graph.infrastructure_graph import graph as infra_graph
from graph.cascade_bfs import cascade_bfs
from routers.ws import manager

router = APIRouter(prefix="/simulation", tags=["simulation"])

# Runtime node status store — mutated by trigger/reset
_node_status: dict[str, str] = {}

FailureType = Literal["main_break", "power_outage", "signal_failure", "capacity_exceeded"]

PRESET_SCENARIOS = [
    {
        "id": "water_34th_break",
        "label": "34th St Water Main Break",
        "node_id": "water_34th",
        "failure_type": "main_break",
        "description": "Rupture at the 34th St junction — primary supply to Midtown hospitals and transit hubs.",
    },
    {
        "id": "times_sq_signal",
        "label": "Times Square Signal Failure",
        "node_id": "transit_times_sq",
        "failure_type": "signal_failure",
        "description": "CBTC signal failure at Times Square — highest-betweenness transit hub in the city.",
    },
    {
        "id": "bellevue_surge",
        "label": "Bellevue Hospital Capacity Surge",
        "node_id": "health_bellevue",
        "failure_type": "capacity_exceeded",
        "description": "Bellevue ER at 140% capacity — ambulance diversion cascades to NYU Langone and Mount Sinai.",
    },
    {
        "id": "fdny_downtown",
        "label": "FDNY Downtown Depletion",
        "node_id": "emergency_fdny_downtown",
        "failure_type": "capacity_exceeded",
        "description": "Multiple simultaneous incidents deplete Downtown FDNY units.",
    },
]


class TriggerRequest(BaseModel):
    node_id: str
    failure_type: FailureType = "main_break"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def _stream_cascade(node_id: str, failure_type: str) -> None:
    """Run BFS and stream cascade_node events with time-scaled delays."""
    events = cascade_bfs(infra_graph.G, node_id)
    if not events:
        return

    # Mark origin as failed immediately
    _node_status[node_id] = "failed"

    await manager.broadcast({
        "type": "cascade_start",
        "payload": {
            "origin_node_id": node_id,
            "failure_type": failure_type,
            "total_predicted_affected": len(events),
            "triggered_at": _now_iso(),
        },
    })

    prev_minutes = 0.0
    speed = max(0.1, settings.CASCADE_PLAYBACK_SPEED)

    for event in events:
        # Sleep proportional to the gap between this event and the previous
        gap = event["predicted_impact_minutes"] - prev_minutes
        # Scale: 1 predicted minute = 1 real second / playback_speed
        sleep_secs = min((gap / speed), 4.0)  # cap at 4s per step for demo fluency
        if sleep_secs > 0.05:
            await asyncio.sleep(sleep_secs)
        prev_minutes = event["predicted_impact_minutes"]

        # Update runtime status
        if event["node_id"] != node_id:
            severity = event["severity"]
            if severity >= 0.7:
                _node_status[event["node_id"]] = "critical"
            elif severity >= 0.4:
                _node_status[event["node_id"]] = "warning"

        await manager.broadcast({
            "type": "cascade_node",
            "payload": {
                **event,
                "status": _node_status.get(event["node_id"], "warning"),
                "timestamp": _now_iso(),
            },
        })

    await manager.broadcast({
        "type": "cascade_complete",
        "payload": {
            "origin_node_id": node_id,
            "total_affected": len(events),
            "completed_at": _now_iso(),
        },
    })


@router.post("/trigger")
async def trigger_cascade(req: TriggerRequest, background_tasks: BackgroundTasks):
    if req.node_id not in infra_graph.G:
        return {"error": f"Node '{req.node_id}' not found in graph"}

    background_tasks.add_task(_stream_cascade, req.node_id, req.failure_type)
    return {
        "status": "cascade_triggered",
        "node_id": req.node_id,
        "failure_type": req.failure_type,
        "triggered_at": _now_iso(),
    }


@router.post("/reset")
async def reset_simulation():
    _node_status.clear()
    await manager.broadcast({
        "type": "simulation_reset",
        "payload": {"reset_at": _now_iso()},
    })
    return {"status": "reset", "reset_at": _now_iso()}


@router.get("/scenarios")
async def get_scenarios():
    return PRESET_SCENARIOS


@router.get("/status")
async def get_node_status():
    """Returns the current runtime status overrides for all affected nodes."""
    return _node_status
