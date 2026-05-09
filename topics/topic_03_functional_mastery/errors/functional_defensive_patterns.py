"""Defensive pipeline execution patterns.

Functional pipelines should validate stage contracts before execution and add
context when a stage fails. ``safe_pipe`` runs k stages in O(k) calls plus stage
cost and stores only the current value, O(1) extra space. It wraps unexpected
stage exceptions in ``FunctionalPipelineError`` while preserving the original
exception as ``__cause__``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .callable_contracts import ensure_callable


class FunctionalPipelineError(RuntimeError):
    """Raised when a functional pipeline stage fails with stage context."""


def safe_pipe(value: Any, *functions: Callable[[Any], Any]) -> Any:
    """Apply functions left-to-right with callable validation and error wrapping."""

    result = value
    for index, function in enumerate(functions):
        ensure_callable(function, f"stage {index}")
        try:
            result = function(result)
        except FunctionalPipelineError:
            raise
        except Exception as exc:  # educational wrapper preserves cause
            stage_name = getattr(function, "__name__", type(function).__name__)
            raise FunctionalPipelineError(f"stage {index} ({stage_name}) failed: {exc}") from exc
    return result
