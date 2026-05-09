"""StopIteration and exhaustion helpers."""
def consume_one(iterator, default=None):
    try:
        return next(iterator)
    except StopIteration:
        return default
