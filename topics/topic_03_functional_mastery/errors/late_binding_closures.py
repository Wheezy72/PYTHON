"""Late-binding closure pitfalls and fixes.

Python closures capture variables, not frozen values. A closure created in a
loop that references the loop variable will observe its final value when later
called. The bad builder demonstrates that bug; fixed builders bind the current
value with a default argument or closure factory.

Building n checkers costs O(n) time and O(n) space. Each checker performs tag
membership: O(t) for list/tuple tags, O(1) average for sets.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


def build_bad_tag_checkers(tags: list[str] | tuple[str, ...]) -> list[Callable[[Mapping[str, Any]], bool]]:
    """Return intentionally broken checkers that all reference the final tag."""

    checkers = []
    for tag in tags:
        def checker(record: Mapping[str, Any]) -> bool:
            return tag in record.get("tags", ())
        checkers.append(checker)
    return checkers


def build_tag_checkers(tags: list[str] | tuple[str, ...]) -> list[Callable[[Mapping[str, Any]], bool]]:
    """Return fixed checkers using default-argument binding."""

    checkers = []
    for tag in tags:
        def checker(record: Mapping[str, Any], expected: str = tag) -> bool:
            return expected in record.get("tags", ())
        checkers.append(checker)
    return checkers


def build_tag_checkers_factory(tags: list[str] | tuple[str, ...]) -> list[Callable[[Mapping[str, Any]], bool]]:
    """Return fixed checkers using a closure factory."""

    def make_checker(expected: str) -> Callable[[Mapping[str, Any]], bool]:
        def checker(record: Mapping[str, Any]) -> bool:
            return expected in record.get("tags", ())
        return checker
    return [make_checker(tag) for tag in tags]
