"""Decorator-based event validators.

Validators inspect mapping-backed event records and return the record unchanged
or raise. Required-field validation is O(r) for r fields. Severity validation
is O(1). Applying v validators is O(v) plus validation cost before the transform
runs.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from functools import wraps
from typing import Any, TypeVar

Record = Mapping[str, Any]
Validator = Callable[[Record], Record]
Transform = TypeVar("Transform", bound=Callable[..., Record])


def validate_event_fields(required_fields: tuple[str, ...] | list[str] | set[str]) -> Validator:
    """Return a validator requiring every named field."""

    required = tuple(required_fields)

    def validator(record: Record) -> Record:
        missing = [field for field in required if field not in record]
        if missing:
            raise KeyError(f"missing required event field(s): {', '.join(missing)}")
        return record
    return validator


def validate_severity_range(min_value: int = 1, max_value: int = 5) -> Validator:
    """Return a validator requiring integer severity in the inclusive range."""

    def validator(record: Record) -> Record:
        severity = record.get("severity")
        if not isinstance(severity, int) or not min_value <= severity <= max_value:
            raise ValueError(f"severity must be an integer between {min_value} and {max_value}")
        return record
    return validator


def validated_transform(*validators: Validator) -> Callable[[Transform], Transform]:
    """Decorate a transform so validators run before the transform."""

    def decorator(func: Transform) -> Transform:
        @wraps(func)
        def wrapper(record: Record, *args: Any, **kwargs: Any) -> Record:
            current = record
            for validator in validators:
                current = validator(current)
            return func(current, *args, **kwargs)
        return wrapper  # type: ignore[return-value]
    return decorator
