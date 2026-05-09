"""KeyError patterns for dictionary-backed event records.

Dictionary key access and get are average O(1). Direct indexing is appropriate
for required fields because it raises KeyError. The get form is appropriate for
optional fields or defensive fallbacks.
"""

from __future__ import annotations


def require_event_field(record: dict[str, object], field: str) -> object:
    """Return a required field, raising KeyError if it is absent."""
    return record[field]


def get_event_field(record: dict[str, object], field: str, default=None) -> object | None:
    """Return a field or default using average O(1) dict lookup."""
    return record.get(field, default)
