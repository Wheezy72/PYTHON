"""Awaitable validation."""
import inspect
def ensure_awaitable(value):
    if not inspect.isawaitable(value):
        raise TypeError("value must be awaitable")
    return value
