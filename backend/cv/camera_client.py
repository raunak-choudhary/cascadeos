"""
NYC DOT traffic camera client with a small in-memory frame cache.
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import urljoin

import httpx

from config import settings
from graph.infrastructure_graph import graph

FRAME_CACHE_SECONDS = 25
CAMERA_CACHE_SECONDS = 300
MAX_CAMERAS = 3


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _pick(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    lowered = {str(k).lower(): v for k, v in data.items()}
    for key in keys:
        value = lowered.get(key.lower())
        if value not in (None, ""):
            return value
    return None


def _float_or_none(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _flatten_camera_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("cameras", "Cameras", "data", "features", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return [payload]


def _distance_km(lat_a: float, lng_a: float, lat_b: float, lng_b: float) -> float:
    radius_km = 6371.0
    d_lat = math.radians(lat_b - lat_a)
    d_lng = math.radians(lng_b - lng_a)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat_a))
        * math.cos(math.radians(lat_b))
        * math.sin(d_lng / 2) ** 2
    )
    return radius_km * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


class CameraClient:
    def __init__(self) -> None:
        self._camera_cache: list[dict[str, Any]] = []
        self._camera_cache_at: datetime | None = None
        self._frame_cache: dict[str, dict[str, Any]] = {}

    async def get_cameras(self, limit: int = MAX_CAMERAS) -> list[dict[str, Any]]:
        if (
            self._camera_cache
            and self._camera_cache_at
            and _now() - self._camera_cache_at < timedelta(seconds=CAMERA_CACHE_SECONDS)
        ):
            return self._camera_cache[:limit]

        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(settings.NYC_DOT_CAMERA_API_URL)
            response.raise_for_status()
            raw_cameras = _flatten_camera_payload(self._parse_payload(response.text))

        cameras = [camera for item in raw_cameras if (camera := self._normalize_camera(item))]
        self._camera_cache = self._prioritize(cameras)
        self._camera_cache_at = _now()
        return self._camera_cache[:limit]

    def _parse_payload(self, text: str) -> Any:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            stripped = text.strip()
            prefix = "window.CAMERAS"
            if stripped.startswith(prefix):
                _, _, value = stripped.partition("=")
                return json.loads(value.rstrip(";").strip())
            raise

    async def get_camera(self, camera_id: str) -> dict[str, Any] | None:
        for camera in await self.get_cameras(limit=2000):
            if camera["id"] == camera_id:
                return camera
        return None

    async def get_latest_frame(self, camera_id: str) -> tuple[bytes, str, str]:
        cached = self._frame_cache.get(camera_id)
        if cached and _now() - cached["timestamp"] < timedelta(seconds=FRAME_CACHE_SECONDS):
            return cached["content"], cached["content_type"], cached["timestamp"].isoformat()

        camera = await self.get_camera(camera_id)
        if not camera or not camera.get("image_url"):
            raise ValueError(f"No frame URL available for camera '{camera_id}'")

        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
            response = await client.get(camera["image_url"])
            response.raise_for_status()
            content_type = response.headers.get("content-type", "image/jpeg").split(";")[0]
            content = response.content

        captured_at = _now()
        self._frame_cache[camera_id] = {
            "content": content,
            "content_type": content_type,
            "timestamp": captured_at,
        }
        return content, content_type, captured_at.isoformat()

    def _normalize_camera(self, raw: dict[str, Any]) -> dict[str, Any] | None:
        props = raw.get("properties") if isinstance(raw.get("properties"), dict) else raw
        geometry = raw.get("geometry") if isinstance(raw.get("geometry"), dict) else {}
        coordinates = geometry.get("coordinates") if isinstance(geometry.get("coordinates"), list) else []

        camera_id = _pick(props, "id", "cameraId", "camera_id", "uuid", "key", "sourceId")
        name = _pick(props, "name", "cameraName", "title", "description", "roadway") or camera_id
        lat = _float_or_none(_pick(props, "lat", "latitude", "Latitude"))
        lng = _float_or_none(_pick(props, "lng", "lon", "longitude", "Longitude"))

        if len(coordinates) >= 2:
            lng = lng if lng is not None else _float_or_none(coordinates[0])
            lat = lat if lat is not None else _float_or_none(coordinates[1])

        if camera_id is None or lat is None or lng is None:
            return None

        image_url = _pick(
            props,
            "imageUrl",
            "image_url",
            "stillImageUrl",
            "url",
            "snapshotUrl",
            "href",
        )
        if image_url and isinstance(image_url, str) and image_url.startswith("/"):
            image_url = urljoin(settings.NYC_DOT_CAMERA_API_URL, image_url)
        if not image_url:
            image_url = urljoin(settings.NYC_DOT_CAMERA_API_URL.rstrip("/") + "/", f"{camera_id}/image")

        return {
            "id": str(camera_id),
            "name": str(name),
            "lat": lat,
            "lng": lng,
            "image_url": str(image_url),
        }

    def _prioritize(self, cameras: list[dict[str, Any]]) -> list[dict[str, Any]]:
        infra_nodes = [
            data
            for _, data in graph.G.nodes(data=True)
            if data.get("lat") is not None and data.get("lng") is not None
        ]

        def score(camera: dict[str, Any]) -> float:
            if not infra_nodes:
                return 0.0
            return min(
                _distance_km(camera["lat"], camera["lng"], node["lat"], node["lng"])
                for node in infra_nodes
            )

        return sorted(cameras, key=score)


camera_client = CameraClient()
