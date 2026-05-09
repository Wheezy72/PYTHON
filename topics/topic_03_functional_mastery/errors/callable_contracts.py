"""Callable contract validation for functional pipelines.

Higher-order code fails unclearly when a non-callable is passed as a stage or
when a transform returns a scalar instead of a record. These helpers raise
precise ``TypeError`` messages at the boundary. Callable checks are O(1).
Copying a mapping result is O(n) time and O(n) space for n fields.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


def ensure_callable(obj: Any, name: str = "callback") -> Callable[..., Any]:
    """Return ``obj`` if callable, otherwise raise a helpful ``TypeError``."""

    if not callable(obj):
        raise TypeError(f"{name} must be callable, got {type(obj).__name__}")
    return obj


def apply_transform(record: Mapping[str, Any], transform: Callable[[Mapping[str, Any]], Mapping[str, Any]]) -> dict[str, Any]:
    """Validate and apply a record transform, returning a dict copy."""

    ensure_callable(transform, "transform")
    result = transform(record)
    if not isinstance(result, Mapping):
        raise TypeError(f"transform must return a mapping-like record, got {type(result).__name__}")
    return dict(result)
