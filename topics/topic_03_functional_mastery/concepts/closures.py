"""Closure-backed SentinelFlow helpers.

Closures keep outer-scope variables alive after a factory returns. SentinelFlow
uses them for local stream state such as counters, source filters, and severity
histograms without global variables. The enclosed state here is intentionally
small and explicit.

Dictionary-backed counts use hash-table lookup/update in O(1) average time and
O(k) space for k distinct severities. Scalar counter updates are O(1) time and
O(1) space. Record field lookup in mapping-backed events is O(1) average. List
or tuple membership would be O(n), while set membership is O(1) average.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping


def make_event_counter() -> Callable[[Mapping[str, object] | None], int]:
    """Return a closure that increments and returns a processed-event count."""

    count = 0

    def count_event(record: Mapping[str, object] | None = None) -> int:
        nonlocal count
        count += 1
        return count

    return count_event


def make_source_filter(source: str) -> Callable[[Mapping[str, object]], bool]:
    """Return a predicate accepting records whose ``source`` equals ``source``."""

    expected = source

    def matches(record: Mapping[str, object]) -> bool:
        return record.get("source") == expected

    return matches


def make_severity_tracker() -> Callable[[Mapping[str, object]], dict[int, int]]:
    """Return a closure that tracks severity frequencies and returns snapshots."""

    counts: dict[int, int] = {}

    def track(record: Mapping[str, object]) -> dict[int, int]:
        severity = record.get("severity")
        if not isinstance(severity, int):
            severity = 0
        counts[severity] = counts.get(severity, 0) + 1
        return dict(counts)

    return track
