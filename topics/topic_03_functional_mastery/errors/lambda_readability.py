"""Deterministic lambda readability checks.

Anonymous predicates are readable when they are tiny. This module uses a small
deterministic heuristic: long snippets or snippets with many logical/structural
markers should be replaced by named helpers. The scan is O(n) over the source
string and O(1) auxiliary space.
"""

from __future__ import annotations

COMPLEX_MARKERS = (" and ", " or ", " if ", " for ", "lambda", "(", ")")


def is_overly_complex_lambda(source: str, max_length: int = 80, max_markers: int = 3) -> bool:
    """Return True when ``source`` is too dense for an anonymous predicate."""

    normalized = " ".join(source.strip().split())
    marker_count = sum(normalized.count(marker) for marker in COMPLEX_MARKERS)
    return len(normalized) > max_length or marker_count > max_markers


def readability_advice(source: str) -> str:
    """Return deterministic advice for a predicate source snippet."""

    if is_overly_complex_lambda(source):
        return "replace with a named predicate helper"
    return "lambda is acceptable for this tiny predicate"


def named_severity_and_tag(minimum: int, tag: str):
    """Return a named replacement for a dense severity/tag predicate."""

    def predicate(record):
        return record.get("severity", 0) >= minimum and tag in record.get("tags", ())
    return predicate
