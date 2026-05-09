"""Hash-backed tag registry for SentinelFlow events.

The registry uses dictionaries of sets: tag -> event ids and event id -> tags.
Adding an event is O(t) average time for t tags. Membership checks are O(1)
average. Returning frozensets copies k entries in O(k), protecting registry state
from caller mutation at the cost of extra space.
"""

from __future__ import annotations

from topics.topic_02_linear_dsa_error_architecture.errors.hashability_type_error import ensure_hashable_tag
from topics.topic_02_linear_dsa_error_architecture.errors.value_error_validation import normalize_event_record


class TagRegistry:
    """Track event ids by tag and tags by event id."""

    def __init__(self) -> None:
        self._events_by_tag: dict[str, set[str]] = {}
        self._tags_by_event: dict[str, set[str]] = {}

    def add_event(self, record: dict[str, object]) -> dict[str, object]:
        """Normalize a record and add its event/tag relationships."""
        normalized = normalize_event_record(record)
        return self.add_normalized(normalized)

    def add_normalized(self, normalized: dict[str, object]) -> dict[str, object]:
        """Add tag relationships for an already-normalized record."""
        event_id = normalized["event_id"]
        tags = {ensure_hashable_tag(tag) for tag in normalized["tags"]}  # type: ignore[union-attr]
        self._tags_by_event[event_id] = tags  # type: ignore[index]
        for tag in tags:
            self._events_by_tag.setdefault(tag, set()).add(event_id)  # type: ignore[arg-type]
        return normalized

    def event_ids_for_tag(self, tag: str) -> frozenset[str]:
        """Return event ids that have tag."""
        normalized = ensure_hashable_tag(tag)
        return frozenset(self._events_by_tag.get(normalized, set()))

    def has_tag(self, event_id: str, tag: str) -> bool:
        """Return whether event_id has tag using average O(1) membership."""
        normalized = ensure_hashable_tag(tag)
        return normalized in self._tags_by_event.get(event_id, set())

    def tags_for_event(self, event_id: str) -> frozenset[str]:
        """Return tags for event_id."""
        return frozenset(self._tags_by_event.get(event_id, set()))

    def all_tags(self) -> frozenset[str]:
        """Return every known tag."""
        return frozenset(self._events_by_tag)
