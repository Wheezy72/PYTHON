"""Defensive iterable validation."""
def ensure_iterable(value):
    try:
        iter(value)
    except TypeError as exc:
        raise TypeError("value must be iterable") from exc
    return value
