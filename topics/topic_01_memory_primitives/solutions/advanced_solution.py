"""Reference solution for the Topic 01 advanced challenge."""

from __future__ import annotations

from collections.abc import Iterable

from ..dsa.memory_inspector import compare_event_memory
from ..dsa.primitive_event import PrimitiveEvent
from ..dsa.tag_index import build_tag_index


def profile_and_index_events(records: Iterable[dict[str, object]]) -> dict[str, object]:
    """Convert records to immutable events, build a tag index, and profile memory."""

    events = tuple(PrimitiveEvent.from_record(record) for record in records)
    tag_index = build_tag_index(events)
    memory_summary = compare_event_memory(events)
    return {
        "events": events,
        "tag_index": tag_index,
        "memory_summary": memory_summary,
    }
