"""Mid solution: validation decorators and configured predicates."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from topics.topic_03_functional_mastery.concepts.lambda_predicates import severity_at_least
from topics.topic_03_functional_mastery.concepts.pure_composition import add_tag, normalize_message
from topics.topic_03_functional_mastery.dsa.decorator_validators import validate_event_fields, validate_severity_range, validated_transform
from topics.topic_03_functional_mastery.dsa.predicate_filters import filter_records

_REQUIRED_FIELDS = ("event_id", "source", "severity", "message")


@validated_transform(validate_event_fields(_REQUIRED_FIELDS), validate_severity_range())
def enrich_valid_event(record: Mapping[str, Any]) -> dict[str, Any]:
    """Return a normalized valid event tagged as validated."""

    return add_tag(normalize_message(record), "validated")


def critical_alerts(records: Iterable[Mapping[str, Any]], minimum: int = 4) -> list[dict[str, Any]]:
    """Return enriched valid events whose severity is at least ``minimum``."""

    enriched = [enrich_valid_event(record) for record in records]
    return list(filter_records(enriched, severity_at_least(minimum)))
