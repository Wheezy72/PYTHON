"""Reusable EventIndex for SentinelFlow records.

EventIndex combines hash tables and append-only grouping lists. Adding one raw
event is O(t + m) for normalization plus average O(1) id/source/severity index
updates. Adding an already-normalized event is O(1) average. Building n events
is O(n) over records plus tag/metadata normalization cost. The indexes use O(n)
space and preserve insertion order inside grouped lists.
"""

from __future__ import annotations

from topics.topic_02_linear_dsa_error_architecture.errors.value_error_validation import normalize_event_record


class EventIndex:
    """Index normalized events by id, source, and severity."""

    def __init__(self) -> None:
        self.by_id: dict[str, dict[str, object]] = {}
        self.by_source: dict[str, list[dict[str, object]]] = {}
        self.by_severity: dict[int, list[dict[str, object]]] = {}

    def add(self, record: dict[str, object]) -> dict[str, object]:
        """Normalize and add one record; raise ValueError for duplicate ids."""
        normalized = normalize_event_record(record)
        return self.add_normalized(normalized)

    def add_normalized(self, normalized: dict[str, object]) -> dict[str, object]:
        """Add an already-normalized record without copying it again."""
        event_id = normalized["event_id"]
        if event_id in self.by_id:
            raise ValueError(f"duplicate event_id: {event_id}")
        source = normalized["source"]
        severity = normalized["severity"]
        self.by_id[event_id] = normalized  # type: ignore[index]
        self.by_source.setdefault(source, []).append(normalized)  # type: ignore[arg-type]
        self.by_severity.setdefault(severity, []).append(normalized)  # type: ignore[arg-type]
        return normalized

    def build(self, records) -> "EventIndex":
        """Add records in order and return self for fluent construction."""
        for record in records:
            self.add(record)
        return self

    def get(self, event_id: str) -> dict[str, object] | None:
        """Return an event by id using average O(1) lookup."""
        return self.by_id.get(event_id)

    def require(self, event_id: str) -> dict[str, object]:
        """Return an event by id or raise KeyError."""
        return self.by_id[event_id]

    def events_for_source(self, source: str) -> tuple[dict[str, object], ...]:
        """Return events for one source in insertion order."""
        return tuple(self.by_source.get(source, ()))

    def events_for_severity(self, severity: int) -> tuple[dict[str, object], ...]:
        """Return events for one severity in insertion order."""
        return tuple(self.by_severity.get(severity, ()))

    def __len__(self) -> int:
        return len(self.by_id)
