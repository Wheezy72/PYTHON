"""Entry challenge solution: build basic SentinelFlow indexes."""

from __future__ import annotations

from topics.topic_02_linear_dsa_error_architecture.dsa.event_index import EventIndex


def build_event_indexes(records) -> dict[str, object]:
    """Normalize records and return id/source/severity indexes."""
    index = EventIndex().build(records)
    return {
        "events": tuple(index.by_id.values()),
        "by_id": dict(index.by_id),
        "by_source": {source: tuple(events) for source, events in index.by_source.items()},
        "by_severity": {severity: tuple(events) for severity, events in index.by_severity.items()},
    }
