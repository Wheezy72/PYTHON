"""IndexError patterns for list-backed event streams.

List indexing is O(1) for valid positions and naturally raises IndexError for
out-of-bounds access. Defensive wrappers add O(1) bounds checks and can return a
safe default where missing positions are expected.
"""

from __future__ import annotations


def get_event_at(events: list[dict[str, object]], index: int) -> dict[str, object]:
    """Return the event at index, letting list indexing raise IndexError."""
    return events[index]


def safe_get_event_at(events: list[dict[str, object]], index: int, default=None) -> dict[str, object] | None:
    """Return a default instead of raising IndexError for invalid positions."""
    try:
        return events[index]
    except IndexError:
        return default
