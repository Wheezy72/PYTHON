"""Small predicate factories and lambda guidance.

Lambdas are useful for tiny predicates passed near their use site. When logic
needs domain language, multiple branches, or reuse, a named helper is clearer
and easier to test.

Filtering scans n records once: O(n * p) time where p is predicate cost, and
O(k) output space for k accepted records. Dictionary field access is O(1)
average. Tag membership is O(t) for list/tuple tags and O(1) average for set
tags.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any

EventPredicate = Callable[[Mapping[str, Any]], bool]


def severity_at_least(minimum: int) -> EventPredicate:
    """Return a predicate accepting records with integer severity >= minimum."""

    return lambda record: isinstance(record.get("severity"), int) and record["severity"] >= minimum


def has_tag(tag: str) -> EventPredicate:
    """Return a predicate accepting records whose tags contain ``tag``."""

    return lambda record: tag in record.get("tags", ())


def filter_events(events: Iterable[Mapping[str, Any]], predicate: EventPredicate) -> list[Mapping[str, Any]]:
    """Return records accepted by ``predicate`` in original order."""

    return [event for event in events if predicate(event)]
