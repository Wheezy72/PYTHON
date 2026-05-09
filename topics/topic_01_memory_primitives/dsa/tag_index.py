"""Hash-table backed tag index for primitive events."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence

from .primitive_event import PrimitiveEvent


def build_tag_index(events: Iterable[PrimitiveEvent]) -> dict[str, list[str]]:
    """Map each tag to event ids.

    Complexity is O(n * t) for n events with up to t tags each. The index uses a
    dictionary, so tag bucket lookup/insert is O(1) average-case.
    """

    index: dict[str, list[str]] = {}
    for event in events:
        for tag in event.tags:
            index.setdefault(tag, []).append(event.event_id)
    return index


def events_with_tag(index: Mapping[str, Sequence[str]], tag: str) -> tuple[str, ...]:
    """Return event ids for ``tag``; O(1) average lookup plus O(k) tuple copy."""

    return tuple(index.get(tag, ()))
