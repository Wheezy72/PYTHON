"""Event streams modeled as Python lists.

Underlying data structure: CPython lists are dynamic arrays. Appending in place is
amortized O(1), random indexing is O(1), and slicing or copying n items is O(n).
This module intentionally returns new lists to avoid aliasing caller-owned event
streams, trading O(n) time and O(n) extra space for safer pipeline boundaries.
"""

from __future__ import annotations


def append_event(stream: list[dict[str, object]], event: dict[str, object]) -> list[dict[str, object]]:
    """Return a copied stream with event appended in O(n) time and O(n) space."""
    copied = list(stream)
    copied.append(event)
    return copied


def slice_recent_events(stream: list[dict[str, object]], limit: int) -> list[dict[str, object]]:
    """Return the most recent limit events using list slicing in O(k) space/time."""
    if limit <= 0:
        return []
    return list(stream[-limit:])


def find_first_event_id(stream: list[dict[str, object]], event_id: str) -> int | None:
    """Return the first matching index by linear scan, O(n) time and O(1) space."""
    for index, event in enumerate(stream):
        if event.get("event_id") == event_id:
            return index
    return None
