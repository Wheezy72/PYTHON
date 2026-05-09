"""Exhaustion demonstrations."""
def is_exhausted(iterator):
    sentinel = object()
    return next(iterator, sentinel) is sentinel
