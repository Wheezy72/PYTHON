"""Decorator metadata loss and preservation.

A wrapper that omits ``functools.wraps`` hides the wrapped function's name,
docstring, and ``__wrapped__`` link. This makes pipeline diagnostics worse. A
safe wrapper copies metadata while adding behavior. Wrapping is O(1), and each
call adds O(1) overhead beyond the wrapped function's own cost.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def unsafe_trace(func: F) -> Callable[..., Any]:
    """Return a wrapper that deliberately loses metadata."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return wrapper


def safe_trace(func: F) -> F:
    """Return a wrapper that preserves metadata with ``functools.wraps``."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return wrapper  # type: ignore[return-value]


def callable_name(func: Callable[..., Any]) -> str:
    """Return a callable's display name for deterministic diagnostics."""

    return getattr(func, "__name__", type(func).__name__)
