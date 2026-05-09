"""Aliasing bugs from shared mutable state.

Reused mutable defaults and shared list references can leak state between
records. ``unsafe_attach_tag`` demonstrates the bug by mutating the existing
record and tag list in place. ``safe_attach_tag`` returns a new record, a new tag
tuple, and a shallow metadata copy. The safe operation is O(t + m).
"""


def unsafe_attach_tag(record: dict[str, object], tag: str) -> dict[str, object]:
    """Mutate ``record['tags']`` in place and return the same record."""

    tags = record["tags"]
    if not isinstance(tags, list):
        raise ValueError("unsafe_attach_tag requires record['tags'] to be a list")
    tags.append(tag)
    return record


def safe_attach_tag(record: dict[str, object], tag: str) -> dict[str, object]:
    """Return a new record with ``tag`` appended without aliasing tag storage."""

    if not isinstance(tag, str) or not tag:
        raise ValueError("tag must be a non-empty string")
    tags = record.get("tags", ())
    if not isinstance(tags, (list, tuple)) or not all(isinstance(item, str) for item in tags):
        raise ValueError("record tags must be a list or tuple of strings")
    metadata = record.get("metadata", {})
    if not isinstance(metadata, dict):
        raise ValueError("record metadata must be a dictionary")

    new_record = dict(record)
    new_record["tags"] = tuple(tags) + (tag,)
    new_record["metadata"] = metadata.copy()
    return new_record
