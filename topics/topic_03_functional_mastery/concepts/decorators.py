"""Decorator utilities for SentinelFlow event functions.

Decorators wrap callables to add cross-cutting behavior. This module uses
``functools.wraps`` so wrapped stages retain metadata such as ``__name__`` and
``__doc__``. That matters for diagnostics in composed pipelines.

Required-field validation scans r field names and uses O(1) average dict
membership for each lookup, so time is O(r) and extra space is O(m) for m
missing field names. Stage annotation copies a dictionary-backed record in
O(n) time and O(n) space for n top-level fields, then appends to a tuple of
stages in O(s) time/space for s prior stage names.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from functools import wraps
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Mapping[str, Any]])


def require_event_fields(required_fields: tuple[str, ...] | list[str] | set[str]) -> Callable[[F], F]:
    """Decorate a transform so missing required event fields raise ``KeyError``."""

    required = tuple(required_fields)

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(record: Mapping[str, Any], *args: Any, **kwargs: Any) -> Mapping[str, Any]:
            missing = [field for field in required if field not in record]
            if missing:
                raise KeyError(f"missing required event field(s): {', '.join(missing)}")
            return func(record, *args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def annotate_stage(stage_name: str) -> Callable[[F], F]:
    """Decorate a transform to copy its result and append a stage marker."""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(record: Mapping[str, Any], *args: Any, **kwargs: Any) -> dict[str, Any]:
            result = dict(func(record, *args, **kwargs))
            stages = tuple(result.get("stages", ()))
            result["stages"] = stages + (stage_name,)
            return result

        return wrapper  # type: ignore[return-value]

    return decorator
