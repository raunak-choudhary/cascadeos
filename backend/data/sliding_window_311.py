"""
311 surge detector — sliding window implemented with collections.deque.
Evicts complaints older than window_seconds, detects surge when count
within the window exceeds surge_threshold for a neighborhood.
"""
from collections import defaultdict, deque
from datetime import datetime, timezone


class SlidingWindow311:
    def __init__(self, window_seconds: int = 600, surge_threshold: int = 8):
        self.window_seconds = window_seconds
        self.surge_threshold = surge_threshold
        # neighborhood_code → deque of (timestamp_utc, complaint_type) tuples
        self._windows: dict[str, deque] = defaultdict(deque)

    def ingest(self, complaints: list[dict]) -> None:
        """Add new complaints. Evict stale entries older than window_seconds."""
        now = datetime.now(timezone.utc).timestamp()
        cutoff = now - self.window_seconds

        for c in complaints:
            nta = c.get("community_board") or c.get("borough") or "UNKNOWN"
            created_raw = c.get("created_date", "")
            try:
                ts = datetime.fromisoformat(created_raw.replace("Z", "+00:00")).timestamp()
            except (ValueError, AttributeError):
                ts = now

            self._windows[nta].append((ts, c.get("complaint_type", "UNKNOWN")))

        # Evict expired entries for every tracked neighborhood
        for nta, window in self._windows.items():
            while window and window[0][0] < cutoff:
                window.popleft()

    def detect_surges(self) -> list[dict]:
        """Return neighborhoods currently in surge with severity score."""
        now = datetime.now(timezone.utc).timestamp()
        cutoff = now - self.window_seconds
        surges = []

        for nta, window in self._windows.items():
            active = [(ts, ct) for ts, ct in window if ts >= cutoff]
            if len(active) < self.surge_threshold:
                continue

            # Dominant complaint type
            from collections import Counter
            type_counts = Counter(ct for _, ct in active)
            dominant = type_counts.most_common(1)[0][0]

            # Severity: 0–10 based on complaint volume above threshold
            severity = min(10.0, 3.0 + (len(active) - self.surge_threshold) * 0.5)

            surges.append({
                "nta_code": nta,
                "complaint_count": len(active),
                "dominant_complaint_type": dominant,
                "severity_score": round(severity, 2),
                "window_seconds": self.window_seconds,
            })

        return sorted(surges, key=lambda x: x["severity_score"], reverse=True)
