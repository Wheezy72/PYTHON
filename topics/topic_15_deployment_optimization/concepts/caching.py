"""Caching deterministic work."""
from functools import lru_cache

@lru_cache(maxsize=128)
def normalized_source(source):
    return source.strip().lower()
