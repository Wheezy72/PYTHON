"""Validation and normalization for rich SentinelFlow event records.

Each record validation is O(t + m), where t is the number of tags and m is the
number of metadata entries copied. Normalization returns a new top-level record,
converts tags to an immutable tuple, and shallow-copies metadata to prevent common
aliasing bugs at ingestion boundaries.
"""

from __future__ import annotations

REQUIRED_FIELDS = ("event_id", "source", "message", "severity", "tags", "metadata")


def _require_non_empty_string(record: dict[str, object], field: str) -> str:
    value = record[field]
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string")
    text = value.strip()
    if not text:
        raise ValueError(f"{field} must be non-empty")
    return text


def _validate_tags(value: object) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple, set)):
        raise TypeError("tags must be a list, tuple, or set")
    normalized: list[str] = []
    for tag in value:
        if not isinstance(tag, str):
            raise TypeError("tags must contain only strings")
        text = tag.strip()
        if not text:
            raise ValueError("tags must be non-empty strings")
        normalized.append(text)
    return tuple(normalized)


def validate_event_record(record: dict[str, object]) -> dict[str, object]:
    """Validate one event record and return it unchanged if it is valid."""
    if not isinstance(record, dict):
        raise TypeError("record must be a dict")
    for field in REQUIRED_FIELDS:
        if field not in record:
            raise KeyError(field)

    _require_non_empty_string(record, "event_id")
    _require_non_empty_string(record, "source")
    _require_non_empty_string(record, "message")

    severity = record["severity"]
    if isinstance(severity, bool) or not isinstance(severity, int):
        raise TypeError("severity must be an integer from 1 to 5")
    if severity < 1 or severity > 5:
        raise ValueError("severity must be from 1 to 5")

    _validate_tags(record["tags"])
    if not isinstance(record["metadata"], dict):
        raise TypeError("metadata must be a dict")
    return record


def normalize_event_record(record: dict[str, object]) -> dict[str, object]:
    """Return an alias-safe normalized event record."""
    validate_event_record(record)
    return {
        "event_id": _require_non_empty_string(record, "event_id"),
        "source": _require_non_empty_string(record, "source"),
        "message": _require_non_empty_string(record, "message"),
        "severity": record["severity"],
        "tags": _validate_tags(record["tags"]),
        "metadata": dict(record["metadata"]),  # type: ignore[arg-type]
    }
