"""
Max-heap alert priority queue implemented from scratch using Python's heapq.
heapq provides a min-heap, so we negate priority to simulate a max-heap.
"""
import heapq
from typing import Any


class AlertPriorityQueue:
    def __init__(self):
        self._heap: list = []
        self._counter = 0  # stable tiebreaker — earlier pushes win on equal priority

    def push(self, alert: dict, priority: float) -> None:
        """Push an alert with a severity priority (0.0–10.0). Higher = processed first."""
        entry = (-priority, self._counter, alert)
        heapq.heappush(self._heap, entry)
        self._counter += 1

    def pop(self) -> dict | None:
        """Return and remove the highest-priority alert. Returns None if empty."""
        if not self._heap:
            return None
        _, _, alert = heapq.heappop(self._heap)
        return alert

    def peek(self) -> dict | None:
        """Return highest-priority alert without removing it."""
        if not self._heap:
            return None
        _, _, alert = self._heap[0]
        return alert

    def size(self) -> int:
        return len(self._heap)

    def to_list(self) -> list[dict]:
        """Return a priority-sorted snapshot without modifying the heap."""
        return [
            alert
            for neg_pri, _, alert in sorted(self._heap)
        ]

    def clear(self) -> None:
        self._heap.clear()
        self._counter = 0
