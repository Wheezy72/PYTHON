"""Closure-backed counters and deterministic limiters.

These helpers demonstrate enclosed integers and dictionaries. Incrementing a
scalar counter is O(1). Updating a key counter is O(1) average because
dictionaries are hash-table backed and O(k) space for k distinct keys. The rate
limiter is deterministic and counts calls rather than wall-clock time.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Hashable, TypeVar

T = TypeVar("T")


def make_counter(start: int = 0) -> Callable[[], int]:
    """Return a closure that increments from ``start`` on each call."""

    count = start

    def next_count() -> int:
        nonlocal count
        count += 1
        return count
    return next_count


def make_key_counter(key_fn: Callable[[T], Hashable]) -> Callable[[T], dict[Hashable, int]]:
    """Return a closure counting items by keys from ``key_fn``."""

    counts: dict[Hashable, int] = {}

    def count_key(value: T) -> dict[Hashable, int]:
        key = key_fn(value)
        counts[key] = counts.get(key, 0) + 1
        return dict(counts)
    return count_key


def make_rate_limiter(limit: int) -> Callable[[T], bool]:
    """Return a deterministic limiter accepting only the first ``limit`` calls."""

    if limit < 0:
        raise ValueError("limit must be non-negative")
    used = 0

    def allow(value: T) -> bool:
        nonlocal used
        if used >= limit:
            return False
        used += 1
        return True
    return allow
