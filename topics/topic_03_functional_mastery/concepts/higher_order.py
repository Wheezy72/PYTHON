"""Higher-order functions for SentinelFlow event transformations.

Higher-order helpers accept callables so mapping, filtering, and counting can
be reused with different event contracts. Transforms should return records,
predicates should return booleans, and key functions should return hashable
values for dictionary-backed grouping.

``map_events`` and ``filter_events`` scan n events: O(n) calls plus callable
cost and O(n) worst-case output space. ``reduce_counts`` performs O(1) average
dict updates per event, so O(n) average time and O(k) space for k unique keys.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any, Hashable


def map_events(events: Iterable[Mapping[str, Any]], transform: Callable[[Mapping[str, Any]], Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    """Apply ``transform`` to every event and return transformed records."""

    return [transform(event) for event in events]


def filter_events(events: Iterable[Mapping[str, Any]], predicate: Callable[[Mapping[str, Any]], bool]) -> list[Mapping[str, Any]]:
    """Return events for which ``predicate`` returns ``True``."""

    return [event for event in events if predicate(event)]


def reduce_counts(events: Iterable[Mapping[str, Any]], key_fn: Callable[[Mapping[str, Any]], Hashable]) -> dict[Hashable, int]:
    """Count events by keys produced by ``key_fn``."""

    counts: dict[Hashable, int] = {}
    for event in events:
        key = key_fn(event)
        counts[key] = counts.get(key, 0) + 1
    return counts
