"""
YOLOv8 detector wrapper.

The active venv may not have the heavy ML dependencies installed. In that case
the detector emits deterministic demo detections so the rest of the CV signal
pipeline can be exercised without crashing the app.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

from config import settings

ANOMALY_CLASSES = {
    "car": "congestion",
    "truck": "congestion",
    "bus": "congestion",
    "person": "crowd_density",
    "traffic light": "stalled_vehicle",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class YOLODetector:
    def __init__(self) -> None:
        self.model_status = "fallback"
        self._model = None
        try:
            from ultralytics import YOLO

            self._model = YOLO(settings.YOLO_MODEL_PATH)
            self.model_status = "yolo"
        except Exception:
            self._model = None

    def analyze(self, frame: bytes, camera: dict[str, Any], frame_timestamp: str | None = None) -> dict[str, Any]:
        if self._model is not None:
            try:
                return self._analyze_with_yolo(frame, camera, frame_timestamp)
            except Exception:
                self.model_status = "fallback"
        return self._fallback_detection(frame, camera, frame_timestamp)

    def _analyze_with_yolo(
        self,
        frame: bytes,
        camera: dict[str, Any],
        frame_timestamp: str | None,
    ) -> dict[str, Any]:
        from io import BytesIO

        from PIL import Image

        image = Image.open(BytesIO(frame)).convert("RGB")
        results = self._model(image, verbose=False)
        names = getattr(results[0], "names", {})
        detections = []
        vehicle_count = 0
        person_count = 0

        for box in results[0].boxes:
            class_id = int(box.cls[0])
            raw_label = names.get(class_id, str(class_id))
            confidence = float(box.conf[0])
            if confidence < 0.45:
                continue
            mapped = ANOMALY_CLASSES.get(raw_label)
            if not mapped:
                continue
            if mapped == "congestion":
                vehicle_count += 1
            if mapped == "crowd_density":
                person_count += 1
            detections.append({
                "class": mapped,
                "confidence": round(confidence, 3),
                "bbox": [round(float(value), 1) for value in box.xyxy[0].tolist()],
                "severity_contribution": round(confidence * 3.0, 2),
            })

        overall = min(10.0, max(vehicle_count * 0.9 + person_count * 0.55, sum(
            detection["severity_contribution"] for detection in detections[:3]
        )))
        anomaly = overall >= 3.0 or len(detections) >= 2
        return {
            "camera_id": camera["id"],
            "camera_name": camera["name"],
            "lat": camera["lat"],
            "lng": camera["lng"],
            "frame_timestamp": frame_timestamp or _now_iso(),
            "frame_width": image.width,
            "frame_height": image.height,
            "detections": detections[:12],
            "anomaly_detected": anomaly,
            "overall_severity": round(overall, 2),
            "model_status": self.model_status,
        }

    def _fallback_detection(
        self,
        frame: bytes,
        camera: dict[str, Any],
        frame_timestamp: str | None,
    ) -> dict[str, Any]:
        digest = hashlib.sha256(frame[:4096] + camera["id"].encode()).digest()
        confidence = round(0.58 + (digest[0] / 255) * 0.32, 3)
        anomaly = digest[1] % 3 == 0
        detections = []
        if anomaly:
            detections.append({
                "class": "congestion",
                "confidence": confidence,
                "bbox": [
                    80 + digest[2] % 80,
                    70 + digest[3] % 60,
                    230 + digest[4] % 120,
                    180 + digest[5] % 80,
                ],
                "severity_contribution": round(confidence * 7.5, 2),
            })

        return {
            "camera_id": camera["id"],
            "camera_name": camera["name"],
            "lat": camera["lat"],
            "lng": camera["lng"],
            "frame_timestamp": frame_timestamp or _now_iso(),
            "frame_width": 640,
            "frame_height": 360,
            "detections": detections,
            "anomaly_detected": anomaly,
            "overall_severity": round(detections[0]["severity_contribution"] if detections else 1.5, 2),
            "model_status": self.model_status,
        }


yolo_detector = YOLODetector()
