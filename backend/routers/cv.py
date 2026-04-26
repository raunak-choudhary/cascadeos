"""
Computer vision camera endpoints and polling loop.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Response

from agents.base_agent import agent_states, alert_queue
from config import settings
from cv.camera_client import camera_client
from cv.yolo_detector import yolo_detector
from routers.ws import manager

router = APIRouter(prefix="/cv", tags=["cv"])

_latest_results: dict[str, dict[str, Any]] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def _emit_cv_alert(result: dict[str, Any]) -> None:
    severity = min(10.0, max(1.0, float(result.get("overall_severity", 1.0))))
    alert = {
        "id": f"cv-{result['camera_id']}-{result['frame_timestamp']}",
        "domain": "emergency",
        "severity": severity,
        "signal": f"CV anomaly detected at {result['camera_name']}",
        "affected_nodes": [],
        "reasoning": (
            f"{len(result.get('detections', []))} visual signal(s) detected near "
            f"{result['lat']:.4f}, {result['lng']:.4f}. Model status: {result.get('model_status')}."
        ),
        "recommended_action": "Dispatch field verification and monitor adjacent infrastructure nodes.",
        "confidence": max((d.get("confidence", 0) for d in result.get("detections", [])), default=0.5),
        "timestamp": _now_iso(),
        "camera": {
            "id": result["camera_id"],
            "name": result["camera_name"],
            "lat": result["lat"],
            "lng": result["lng"],
        },
    }
    alert_queue.push(alert, priority=severity)
    agent_states.setdefault("emergency", {"domain": "emergency"})
    agent_states["emergency"].update({
        "domain": "emergency",
        "status": "alert" if severity >= 7 else "analyzing",
        "last_signal": alert["signal"],
        "last_reasoning": alert["reasoning"],
        "confidence": alert["confidence"],
        "last_updated": _now_iso(),
    })
    await manager.broadcast({"type": "alert", "payload": alert})
    await manager.broadcast({"type": "agent_update", "payload": agent_states["emergency"]})
    await manager.broadcast({"type": "queue_snapshot", "payload": alert_queue.to_list()[:10]})


async def poll_cv_once() -> list[dict[str, Any]]:
    cameras = await camera_client.get_cameras(limit=3)
    results = []
    for camera in cameras:
        content, _, captured_at = await camera_client.get_latest_frame(camera["id"])
        result = yolo_detector.analyze(content, camera, captured_at)
        _latest_results[camera["id"]] = result
        results.append(result)
        await manager.broadcast({
            "type": "cv_update",
            "payload": {
                **result,
                "frame_url": f"/cv/latest-frame/{camera['id']}?t={int(datetime.now().timestamp())}",
            },
        })
        if result.get("anomaly_detected"):
            await _emit_cv_alert(result)
    return results


async def run_cv_monitor() -> None:
    if not settings.ENABLE_CV:
        return
    while True:
        try:
            await poll_cv_once()
        except Exception as exc:
            await manager.broadcast({
                "type": "cv_status",
                "payload": {
                    "status": "error",
                    "message": str(exc),
                    "timestamp": _now_iso(),
                },
            })
        await asyncio.sleep(max(5, settings.CV_POLL_INTERVAL))


@router.get("/cameras")
async def get_cameras() -> list[dict[str, Any]]:
    return await camera_client.get_cameras(limit=3)


@router.get("/latest")
async def get_latest_results() -> list[dict[str, Any]]:
    return list(_latest_results.values())


@router.post("/poll")
async def poll_now() -> dict[str, Any]:
    results = await poll_cv_once()
    return {"status": "ok", "results": results}


@router.get("/latest-frame/{camera_id}")
async def get_latest_frame(camera_id: str) -> Response:
    try:
        content, content_type, _ = await camera_client.get_latest_frame(camera_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(content=content, media_type=content_type)
