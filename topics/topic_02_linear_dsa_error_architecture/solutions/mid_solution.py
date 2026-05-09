"""Mid challenge solution: tag registry construction and tag filtering."""

from __future__ import annotations

from topics.topic_02_linear_dsa_error_architecture.concepts.set_membership import events_matching_all_tags
from topics.topic_02_linear_dsa_error_architecture.dsa.tag_registry import TagRegistry


def build_tag_registry(records) -> TagRegistry:
    """Normalize records into a hash-backed tag registry."""
    registry = TagRegistry()
    for record in records:
        registry.add_event(record)
    return registry


def filter_events_by_tags(records, required_tags) -> tuple[dict[str, object], ...]:
    """Return normalized records that contain all required tags."""
    normalized_records = []
    registry = TagRegistry()
    for record in records:
        normalized_records.append(registry.add_event(record))
    return tuple(events_matching_all_tags(normalized_records, required_tags))
