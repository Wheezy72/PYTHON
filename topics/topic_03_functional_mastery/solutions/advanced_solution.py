"""Advanced solution: defensive SentinelFlow functional ingestion."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from functools import partial
from typing import Any

from topics.topic_03_functional_mastery.concepts.decorators import annotate_stage
from topics.topic_03_functional_mastery.concepts.partial_application import make_region_enricher
from topics.topic_03_functional_mastery.concepts.pure_composition import add_tag, normalize_message, pipe
from topics.topic_03_functional_mastery.dsa.closure_counters import make_counter, make_key_counter
from topics.topic_03_functional_mastery.dsa.decorator_validators import validate_event_fields, validate_severity_range, validated_transform
from topics.topic_03_functional_mastery.errors.functional_defensive_patterns import FunctionalPipelineError, safe_pipe

_REQUIRED_FIELDS = ("event_id", "source", "severity", "message", "tags")


def _normalize_tags(record: Mapping[str, Any]) -> dict[str, Any]:
    updated = dict(record)
    tags = updated.get("tags", ())
    if isinstance(tags, str):
        tags = (tags,)
    updated["tags"] = tuple(tags or ())
    if isinstance(updated.get("metadata"), Mapping):
        updated["metadata"] = dict(updated["metadata"])
    return updated


@annotate_stage("validated")
@validated_transform(validate_event_fields(_REQUIRED_FIELDS), validate_severity_range())
def _validated_copy(record: Mapping[str, Any]) -> dict[str, Any]:
    return dict(record)


def _prepare_event(record: Mapping[str, Any]) -> dict[str, Any]:
    region = "unknown"
    metadata = record.get("metadata")
    if isinstance(metadata, Mapping):
        region = str(metadata.get("region", region))
    return pipe(record, _normalize_tags, _validated_copy, normalize_message, partial(add_tag, tag="ingested"), make_region_enricher(region))


def run_functional_ingestion(records: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Run a full defensive ingestion pipeline over SentinelFlow event records."""

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    accepted_counter = make_counter(0)
    source_counter = make_key_counter(lambda record: record.get("source", "unknown"))
    counts_by_source: dict[object, int] = {}

    for index, record in enumerate(records):
        try:
            event = safe_pipe(record, _prepare_event)
        except (FunctionalPipelineError, KeyError, ValueError, TypeError) as exc:
            rejected.append({"index": index, "error": str(exc), "record": dict(record)})
            continue
        accepted_counter()
        counts_by_source = source_counter(event)
        accepted.append(event)

    return {"events": accepted, "counts_by_source": counts_by_source, "accepted_count": len(accepted), "rejected": rejected}
