"""Defensive lookup helpers for dictionary indexes.

Dictionary lookup is average O(1), while checking k keys is O(k) average time.
These helpers make optional, required, and batch-missing lookup behavior explicit
instead of mixing KeyError control flow throughout the ingestion pipeline.
"""

from __future__ import annotations


def safe_lookup(index: dict[str, object], key: str, default=None):
    """Return index[key] or default using dict.get."""
    return index.get(key, default)


def require_lookup(index: dict[str, object], key: str):
    """Return index[key], raising KeyError if key is absent."""
    return index[key]


def collect_missing_keys(index: dict[str, object], keys) -> list[str]:
    """Return keys that are absent from index, preserving query order."""
    return [key for key in keys if key not in index]
