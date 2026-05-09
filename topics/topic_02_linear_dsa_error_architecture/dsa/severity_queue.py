"""SeverityQueue backed by collections.deque.

The queue stores normalized records in FIFO order. Enqueue, dequeue, and peek are
O(1). Enqueueing a raw record first normalizes in O(t + m); enqueueing an
already-normalized record keeps the same object reference. drain_min_severity
scans the queue once, so it is O(n) time and O(n) extra space for the returned
alerts plus temporarily retained lower-severity records.
"""

from __future__ import annotations

from collections import deque

from topics.topic_02_linear_dsa_error_architecture.errors.value_error_validation import normalize_event_record


class SeverityQueue:
    """FIFO queue for normalized SentinelFlow events."""

    def __init__(self) -> None:
        self._queue: deque[dict[str, object]] = deque()

    def enqueue(self, record: dict[str, object]) -> dict[str, object]:
        """Normalize and enqueue one record."""
        normalized = normalize_event_record(record)
        return self.enqueue_normalized(normalized)

    def enqueue_normalized(self, normalized: dict[str, object]) -> dict[str, object]:
        """Enqueue an already-normalized record without copying it again."""
        self._queue.append(normalized)
        return normalized

    def dequeue(self) -> dict[str, object] | None:
        """Return the oldest record or None when empty."""
        if not self._queue:
            return None
        return self._queue.popleft()

    def peek(self) -> dict[str, object] | None:
        """Return the oldest record without removing it."""
        if not self._queue:
            return None
        return self._queue[0]

    def drain_min_severity(self, min_severity: int) -> tuple[dict[str, object], ...]:
        """Drain once, returning events whose severity is at least min_severity."""
        alerts: list[dict[str, object]] = []
        retained: deque[dict[str, object]] = deque()
        while self._queue:
            record = self._queue.popleft()
            if record["severity"] >= min_severity:  # type: ignore[operator]
                alerts.append(record)
            else:
                retained.append(record)
        self._queue = retained
        return tuple(alerts)

    def __len__(self) -> int:
        return len(self._queue)
