"""Suppression policy helpers."""
def should_suppress(exc_type, allowed):
    return exc_type is not None and any(issubclass(exc_type, item) for item in allowed)
