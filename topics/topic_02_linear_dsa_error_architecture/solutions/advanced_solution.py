"""Advanced challenge solution: ingest and index SentinelFlow events."""

from __future__ import annotations

from topics.topic_02_linear_dsa_error_architecture.dsa.event_index import EventIndex
from topics.topic_02_linear_dsa_error_architecture.dsa.severity_queue import SeverityQueue
from topics.topic_02_linear_dsa_error_architecture.dsa.tag_registry import TagRegistry
from topics.topic_02_linear_dsa_error_architecture.errors.value_error_validation import normalize_event_record


def ingest_sentinelflow_events(records, min_alert_severity: int = 4) -> dict[str, object]:
    """Normalize records, preserve ingestion order, and build query structures."""
    index = EventIndex()
    registry = TagRegistry()
    queue = SeverityQueue()
    accepted: list[dict[str, object]] = []
    errors: list[dict[str, object]] = []

    for position, record in enumerate(records):
        try:
            normalized = normalize_event_record(record)
            index.add_normalized(normalized)
            registry.add_normalized(normalized)
            queue.enqueue_normalized(normalized)
            accepted.append(normalized)
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(
                {
                    "position": position,
                    "event_id": record.get("event_id") if isinstance(record, dict) else None,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )

    alerts = queue.drain_min_severity(min_alert_severity)
    severity_counts = {
        severity: len(events)
        for severity, events in index.by_severity.items()
    }
    summary = {
        "total_events": len(accepted),
        "source_count": len(index.by_source),
        "tag_count": len(registry.all_tags()),
        "alert_count": len(alerts),
        "severity_counts": severity_counts,
    }
    return {
        "events": tuple(accepted),
        "index": index,
        "registry": registry,
        "event_ids": tuple(event["event_id"] for event in accepted),
        "by_id": dict(index.by_id),
        "by_source": {source: tuple(events) for source, events in index.by_source.items()},
        "by_severity": {severity: tuple(events) for severity, events in index.by_severity.items()},
        "tag_registry": registry,
        "alerts": alerts,
        "summary": summary,
        "errors": tuple(errors),
        "remaining_queue_size": len(queue),
    }
