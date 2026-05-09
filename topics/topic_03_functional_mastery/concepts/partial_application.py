"""Configured transforms with partial application and closures.

Partial application binds configuration now so a later pipeline stage can use a
simple one-argument callable. SentinelFlow uses this for constant enrichment,
message prefixes, and region-specific transforms.

Each helper copies the top-level dictionary in O(n) time and O(n) space for n
fields. String prefixing is O(p + m) for prefix and message lengths. Nested
structures are reused unless explicitly replaced by the transform.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from functools import partial
from typing import Any


def add_constant_field(record: Mapping[str, Any], key: str, value: Any) -> dict[str, Any]:
    """Return a copy of ``record`` with ``key`` set to ``value``."""

    updated = dict(record)
    updated[key] = value
    return updated


def prefix_message(prefix: str, record: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy of ``record`` with ``prefix`` prepended to its message."""

    updated = dict(record)
    updated["message"] = f"{prefix}{record.get('message', '')}"
    return updated


def make_region_enricher(region: str) -> Callable[[Mapping[str, Any]], dict[str, Any]]:
    """Return a configured transform that adds a ``region`` field."""

    return partial(add_constant_field, key="region", value=region)
