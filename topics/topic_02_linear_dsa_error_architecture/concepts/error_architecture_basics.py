"""Error taxonomy for SentinelFlow event validation.

Error architecture is not a data structure, but classification is normally O(1):
it inspects the exception type and message prefix. Clear categories separate
missing fields (KeyError), invalid values (ValueError), invalid shapes/types
(TypeError), bounds errors (IndexError), and unknown failures.
"""

from __future__ import annotations


class EventValidationError(ValueError):
    """Raised when an event has the right shape but invalid values."""


class EventShapeError(TypeError):
    """Raised when an event has the wrong container or field type."""


def classify_exception(exc: Exception) -> str:
    """Classify common validation exceptions into stable categories."""
    message = str(exc).lower()
    if isinstance(exc, KeyError):
        return "missing-field"
    if isinstance(exc, IndexError):
        return "bounds"
    if isinstance(exc, TypeError):
        return "invalid-type"
    if isinstance(exc, ValueError):
        if "missing" in message:
            return "missing-field"
        return "invalid-value"
    return "unknown"
