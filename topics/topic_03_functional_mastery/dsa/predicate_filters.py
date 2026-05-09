"""Predicate combinators and partition helpers.

Predicate combinators run over p predicates and short-circuit. Filtering n
records is O(n * predicate_cost), with O(k) output space. Partition stores both
accepted and rejected records, O(n) space.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")
Predicate = Callable[[T], bool]


def all_of(*predicates: Predicate[T]) -> Predicate[T]:
    """Return a predicate requiring every predicate to accept the value."""

    return lambda value: all(predicate(value) for predicate in predicates)


def any_of(*predicates: Predicate[T]) -> Predicate[T]:
    """Return a predicate requiring at least one predicate to accept the value."""

    return lambda value: any(predicate(value) for predicate in predicates)


def not_(predicate: Predicate[T]) -> Predicate[T]:
    """Return the logical negation of ``predicate``."""

    return lambda value: not predicate(value)


def filter_records(records: Iterable[T], predicate: Predicate[T]) -> list[T]:
    """Return records accepted by ``predicate``."""

    return [record for record in records if predicate(record)]


def partition_records(records: Iterable[T], predicate: Predicate[T]) -> tuple[list[T], list[T]]:
    """Return ``(accepted, rejected)`` lists while preserving order."""

    accepted: list[T] = []
    rejected: list[T] = []
    for record in records:
        (accepted if predicate(record) else rejected).append(record)
    return accepted, rejected
