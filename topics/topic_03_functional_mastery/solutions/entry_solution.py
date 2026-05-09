"""Entry solution: pure transform pipeline for SentinelFlow records."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from functools import partial
from typing import Any

from topics.topic_03_functional_mastery.concepts.pure_composition import add_tag, cap_severity, normalize_message, pipe


def build_entry_pipeline(records: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Normalize messages, cap severity, and add a processed tag without mutation."""

    return [pipe(record, normalize_message, partial(cap_severity, maximum=5), partial(add_tag, tag="processed")) for record in records]
