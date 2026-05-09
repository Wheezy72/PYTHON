"""Immutable SentinelFlow primitive event data structure.

``PrimitiveEvent`` uses a frozen, slotted dataclass for compact immutable event
records. Construction validates and normalizes input in O(t + m), where t is the
number of tags and m is the number of top-level metadata entries. Field lookup is
O(1), appending a tag creates a new tuple/event in O(t), and record conversion is
O(t + m).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from ..errors.event_validation import normalize_event_record


@dataclass(frozen=True, slots=True)
class PrimitiveEvent:
    """Immutable event primitive with aliasing-safe tags and metadata."""

    event_id: str
    source: str
    severity: int
    message: str
    tags: tuple[str, ...] = ()
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        record = {
            "event_id": self.event_id,
            "source": self.source,
            "severity": self.severity,
            "message": self.message,
            "tags": self.tags,
            "metadata": dict(self.metadata),
        }
        normalized = normalize_event_record(record)
        object.__setattr__(self, "event_id", normalized["event_id"])
        object.__setattr__(self, "source", normalized["source"])
        object.__setattr__(self, "severity", normalized["severity"])
        object.__setattr__(self, "message", normalized["message"])
        object.__setattr__(self, "tags", normalized["tags"])
        object.__setattr__(self, "metadata", MappingProxyType(dict(normalized["metadata"])))

    def to_record(self) -> dict[str, object]:
        """Return an aliasing-safe dict copy in O(t + m)."""

        return {
            "event_id": self.event_id,
            "source": self.source,
            "severity": self.severity,
            "message": self.message,
            "tags": tuple(self.tags),
            "metadata": dict(self.metadata),
        }

    def with_tag(self, tag: str) -> "PrimitiveEvent":
        """Return a new event with ``tag`` appended in O(t)."""

        if not isinstance(tag, str) or not tag:
            raise ValueError("tag must be a non-empty string")
        return PrimitiveEvent(
            self.event_id,
            self.source,
            self.severity,
            self.message,
            self.tags + (tag,),
            dict(self.metadata),
        )

    @classmethod
    def from_record(cls, record: Mapping[str, object]) -> "PrimitiveEvent":
        """Create an event from a mapping after defensive normalization."""

        normalized = normalize_event_record(dict(record))
        return cls(
            event_id=normalized["event_id"],  # type: ignore[arg-type]
            source=normalized["source"],  # type: ignore[arg-type]
            severity=normalized["severity"],  # type: ignore[arg-type]
            message=normalized["message"],  # type: ignore[arg-type]
            tags=normalized["tags"],  # type: ignore[arg-type]
            metadata=normalized["metadata"],  # type: ignore[arg-type]
        )
