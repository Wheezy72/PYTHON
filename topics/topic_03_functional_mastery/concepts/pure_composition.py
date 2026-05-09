"""Pure transformations and composition helpers.

Pure functions return new values rather than mutating input records. For
SentinelFlow dictionaries, that means copying top-level fields and replacing
changed nested values such as tags or metadata so caller-owned mutable
containers do not leak into pipeline output.

Dictionary copies are O(f) time and O(f) space for f fields. Tag tuple copies
are O(t) time and O(t) space. Metadata shallow copies are O(m). Composition
over k functions stores O(k) stages and runs O(k) calls plus stage costs.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, TypeVar

T = TypeVar("T")


def _copy_record(record: Mapping[str, Any]) -> dict[str, Any]:
    copied = dict(record)
    if "tags" in copied:
        copied["tags"] = tuple(copied.get("tags") or ())
    if isinstance(copied.get("metadata"), Mapping):
        copied["metadata"] = dict(copied["metadata"])
    return copied


def normalize_message(record: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy with collapsed whitespace and lowercase message text."""

    copied = _copy_record(record)
    copied["message"] = " ".join(str(copied.get("message", "")).strip().lower().split())
    return copied


def cap_severity(record: Mapping[str, Any], maximum: int = 5) -> dict[str, Any]:
    """Return a copy with integer severity capped to ``maximum``."""

    copied = _copy_record(record)
    severity = copied.get("severity", 0)
    if isinstance(severity, int):
        copied["severity"] = min(severity, maximum)
    return copied


def add_tag(record: Mapping[str, Any], tag: str) -> dict[str, Any]:
    """Return a copy with ``tag`` appended once to tuple-backed tags."""

    copied = _copy_record(record)
    tags = tuple(copied.get("tags") or ())
    copied["tags"] = tags if tag in tags else tags + (tag,)
    return copied


def compose(*functions: Callable[[T], T]) -> Callable[[T], T]:
    """Compose unary functions right-to-left."""

    stages = tuple(functions)

    def composed(value: T) -> T:
        result = value
        for function in reversed(stages):
            result = function(result)
        return result

    return composed


def pipe(value: T, *functions: Callable[[T], T]) -> T:
    """Apply unary functions left-to-right to ``value``."""

    result = value
    for function in functions:
        result = function(result)
    return result
