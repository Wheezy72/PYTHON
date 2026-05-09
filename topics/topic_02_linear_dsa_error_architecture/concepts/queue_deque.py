"""FIFO event queues backed by collections.deque.

Underlying data structure: deque is a block-linked double-ended queue. Appends
and pops at either end are O(1), while indexing or searching is O(n). It uses more
pointer overhead than a compact list but avoids O(n) front-removal shifts.
"""

from __future__ import annotations

from collections import deque


def enqueue_event(queue: deque[dict[str, object]], event: dict[str, object]) -> deque[dict[str, object]]:
    """Append an event to the right side of the queue in O(1)."""
    queue.append(event)
    return queue


def dequeue_event(queue: deque[dict[str, object]]) -> dict[str, object] | None:
    """Pop the oldest event in O(1), returning None when the queue is empty."""
    if not queue:
        return None
    return queue.popleft()


def drain_queue(queue: deque[dict[str, object]], limit: int | None = None) -> list[dict[str, object]]:
    """Drain up to limit events from the queue in O(k) time and space."""
    drained: list[dict[str, object]] = []
    while queue and (limit is None or len(drained) < limit):
        drained.append(queue.popleft())
    return drained
