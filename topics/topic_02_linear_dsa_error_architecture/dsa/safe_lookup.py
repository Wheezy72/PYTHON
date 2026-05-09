"""Small required/optional lookup helpers for SentinelFlow indexes.

The helpers wrap dictionary lookup semantics. Optional lookups are average O(1),
and require_all is O(k) for k requested keys plus O(k) output space. Missing keys
are reported together to make ingestion errors easier to act on.
"""

from __future__ import annotations

from topics.topic_02_linear_dsa_error_architecture.errors.defensive_lookup import collect_missing_keys, require_lookup, safe_lookup


def find_or_none(index: dict[str, object], key: str):
    """Return index[key] or None."""
    return safe_lookup(index, key)


def find_or_default(index: dict[str, object], key: str, default):
    """Return index[key] or default."""
    return safe_lookup(index, key, default)


def require_all(index: dict[str, object], keys) -> dict[str, object]:
    """Return all requested key/value pairs or raise KeyError listing misses."""
    missing = collect_missing_keys(index, keys)
    if missing:
        raise KeyError(f"missing keys: {', '.join(missing)}")
    return {key: require_lookup(index, key) for key in keys}
