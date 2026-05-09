"""Defensive validation for primitive event records.

Primitive records are plain dictionaries, so callers can omit fields or provide
values with the wrong type. Missing required fields raise ``KeyError`` because
the record shape is incomplete. Invalid present values raise ``ValueError``.
Validation is O(t + m) where t is the number of tags and m is top-level metadata
size when normalization copies metadata.
"""

REQUIRED_EVENT_FIELDS = ("event_id", "source", "severity", "message", "tags", "metadata")


def _non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_event_record(record: dict[str, object]) -> dict[str, object]:
    """Validate and return the original event record.

    Raises ``KeyError`` for a missing required field and ``ValueError`` for an
    invalid value. Tags must be a list or tuple of strings; metadata must be a
    dictionary.
    """

    for field in REQUIRED_EVENT_FIELDS:
        if field not in record:
            raise KeyError(field)

    for field in ("event_id", "source", "message"):
        if not _non_empty_string(record[field]):
            raise ValueError(f"{field} must be a non-empty string")

    severity = record["severity"]
    if not isinstance(severity, int) or isinstance(severity, bool) or not 1 <= severity <= 5:
        raise ValueError("severity must be an integer from 1 through 5")

    tags = record["tags"]
    if not isinstance(tags, (list, tuple)) or not all(isinstance(tag, str) for tag in tags):
        raise ValueError("tags must be a list or tuple of strings")

    if not isinstance(record["metadata"], dict):
        raise ValueError("metadata must be a dictionary")

    return record


def normalize_event_record(record: dict[str, object]) -> dict[str, object]:
    """Validate and return an aliasing-safe normalized event record."""

    validate_event_record(record)
    return {
        "event_id": record["event_id"],
        "source": record["source"],
        "severity": record["severity"],
        "message": record["message"],
        "tags": tuple(record["tags"]),  # type: ignore[arg-type]
        "metadata": dict(record["metadata"]),  # type: ignore[arg-type]
    }
