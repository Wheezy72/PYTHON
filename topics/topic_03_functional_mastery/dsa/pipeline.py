"""Generic pipeline composition data structures.

A pipeline stores a tuple of callable stages. Tuple storage is immutable and
compact: O(k) space for k stages. Calling a pipeline is O(k) stage invocations
plus each stage's own cost. Validation checks each stage once, O(k).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Generic, TypeVar

T = TypeVar("T")


def _validate_stage(stage: Callable[[T], T], index: int) -> Callable[[T], T]:
    if not callable(stage):
        raise TypeError(f"stage {index} must be callable")
    return stage


def compose(*functions: Callable[[T], T]) -> Callable[[T], T]:
    """Return a right-to-left composition of unary functions."""

    stages = tuple(_validate_stage(function, index) for index, function in enumerate(functions))

    def composed(value: T) -> T:
        result = value
        for function in reversed(stages):
            result = function(result)
        return result
    return composed


def pipe(value: T, *functions: Callable[[T], T]) -> T:
    """Apply unary functions left-to-right to ``value``."""

    result = value
    for index, function in enumerate(functions):
        result = _validate_stage(function, index)(result)
    return result


class Pipeline(Generic[T]):
    """Callable immutable sequence of unary stages."""

    def __init__(self, stages: Iterable[Callable[[T], T]] = ()) -> None:
        self.stages = tuple(_validate_stage(stage, index) for index, stage in enumerate(stages))

    def __call__(self, value: T) -> T:
        result = value
        for stage in self.stages:
            result = stage(result)
        return result

    def then(self, stage: Callable[[T], T]) -> "Pipeline[T]":
        """Return a new pipeline with ``stage`` appended."""

        _validate_stage(stage, len(self.stages))
        return Pipeline((*self.stages, stage))

    def __len__(self) -> int:
        return len(self.stages)
