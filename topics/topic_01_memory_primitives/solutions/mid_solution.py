"""Reference solution for the Topic 01 mid challenge."""

from ..errors.aliasing_shared_state import safe_attach_tag
from ..errors.event_validation import normalize_event_record


def prepare_event(record: dict[str, object]) -> dict[str, object]:
    """Validate and normalize a primitive event record."""

    return normalize_event_record(record)


def add_tag_without_aliasing(record: dict[str, object], tag: str) -> dict[str, object]:
    """Attach ``tag`` while returning a new aliasing-safe record."""

    return safe_attach_tag(record, tag)
