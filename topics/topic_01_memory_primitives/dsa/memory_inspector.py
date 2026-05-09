"""Memory profiling helpers for primitive events."""

from __future__ import annotations

from collections.abc import Sequence

from ..concepts.memory_measurement import deep_size, shallow_size
from .primitive_event import PrimitiveEvent


def event_memory_profile(event: PrimitiveEvent) -> dict[str, int]:
    """Return shallow/deep byte estimates for event views and fields."""

    record = event.to_record()
    return {
        "record_shallow_size": shallow_size(record),
        "record_deep_size": deep_size(record),
        "tags_shallow_size": shallow_size(event.tags),
        "tags_deep_size": deep_size(event.tags),
        "metadata_shallow_size": shallow_size(event.metadata),
        "metadata_deep_size": deep_size(event.metadata),
        "message_shallow_size": shallow_size(event.message),
        "message_deep_size": deep_size(event.message),
    }


def compare_event_memory(events: Sequence[PrimitiveEvent]) -> dict[str, int | float]:
    """Summarize deep memory estimates for a sequence of events."""

    if not events:
        return {
            "count": 0,
            "total_deep_size": 0,
            "average_deep_size": 0.0,
            "max_deep_size": 0,
        }

    sizes = [event_memory_profile(event)["record_deep_size"] for event in events]
    total = sum(sizes)
    return {
        "count": len(events),
        "total_deep_size": total,
        "average_deep_size": total / len(events),
        "max_deep_size": max(sizes),
    }
