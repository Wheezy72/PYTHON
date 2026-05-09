"""Tests for Topic 02: Linear DSA & Error Architecture."""

from __future__ import annotations

import unittest
from collections import deque
from pathlib import Path

from topics.topic_02_linear_dsa_error_architecture.concepts.big_o_tradeoffs import (
    complexity_table,
    recommend_structure,
)
from topics.topic_02_linear_dsa_error_architecture.concepts.dict_hash_table import (
    build_id_index,
    build_source_index,
    lookup_event,
)
from topics.topic_02_linear_dsa_error_architecture.concepts.error_architecture_basics import (
    classify_exception,
)
from topics.topic_02_linear_dsa_error_architecture.concepts.list_internals import (
    append_event,
    find_first_event_id,
    slice_recent_events,
)
from topics.topic_02_linear_dsa_error_architecture.concepts.queue_deque import (
    dequeue_event,
    drain_queue,
    enqueue_event,
)
from topics.topic_02_linear_dsa_error_architecture.concepts.set_membership import (
    events_matching_all_tags,
    normalize_tag_set,
    unique_tags,
)
from topics.topic_02_linear_dsa_error_architecture.dsa.event_index import EventIndex
from topics.topic_02_linear_dsa_error_architecture.dsa.safe_lookup import (
    find_or_default,
    find_or_none,
    require_all,
)
from topics.topic_02_linear_dsa_error_architecture.dsa.severity_queue import SeverityQueue
from topics.topic_02_linear_dsa_error_architecture.dsa.tag_registry import TagRegistry
from topics.topic_02_linear_dsa_error_architecture.errors.defensive_lookup import (
    collect_missing_keys,
    require_lookup,
    safe_lookup,
)
from topics.topic_02_linear_dsa_error_architecture.errors.hashability_type_error import (
    build_tag_membership,
    ensure_hashable_tag,
)
from topics.topic_02_linear_dsa_error_architecture.errors.index_error_patterns import (
    get_event_at,
    safe_get_event_at,
)
from topics.topic_02_linear_dsa_error_architecture.errors.key_error_patterns import (
    get_event_field,
    require_event_field,
)
from topics.topic_02_linear_dsa_error_architecture.errors.value_error_validation import (
    normalize_event_record,
    validate_event_record,
)
from topics.topic_02_linear_dsa_error_architecture.solutions.advanced_solution import (
    ingest_sentinelflow_events,
)
from topics.topic_02_linear_dsa_error_architecture.solutions.entry_solution import (
    build_event_indexes,
)
from topics.topic_02_linear_dsa_error_architecture.solutions.mid_solution import (
    build_tag_registry,
    filter_events_by_tags,
)


def sentinel_record(
    event_id: str = "evt-1001",
    source: str = "sensor.edge-7",
    severity: int = 3,
    message: str = "temperature threshold crossed",
    tags=None,
    metadata=None,
) -> dict[str, object]:
    return {
        "event_id": event_id,
        "source": source,
        "severity": severity,
        "message": message,
        "tags": ["edge", "temperature"] if tags is None else tags,
        "metadata": {"region": "eu-west", "device_id": "edge-7"} if metadata is None else metadata,
    }


class ConceptTests(unittest.TestCase):
    def test_core_linear_structure_helpers(self) -> None:
        events = [
            sentinel_record("evt-1"),
            sentinel_record("evt-2", "auth.gateway", 5, tags=["security", "alert"]),
            sentinel_record("evt-3", tags=["edge", "heartbeat"]),
        ]

        appended = append_event(events[:1], events[1])
        self.assertEqual([event["event_id"] for event in appended], ["evt-1", "evt-2"])
        self.assertEqual([event["event_id"] for event in slice_recent_events(events, 2)], ["evt-2", "evt-3"])
        self.assertEqual(find_first_event_id(events, "evt-2"), 1)

        by_id = build_id_index(events)
        self.assertIs(lookup_event(by_id, "evt-1"), events[0])
        self.assertEqual(build_source_index(events)["sensor.edge-7"], [events[0], events[2]])

        queue: deque[dict[str, object]] = deque()
        enqueue_event(queue, events[0])
        enqueue_event(queue, events[1])
        self.assertIs(dequeue_event(queue), events[0])
        self.assertEqual(drain_queue(queue), [events[1]])

        table = complexity_table()
        self.assertEqual(table["set"]["membership"], "O(1) average")
        self.assertEqual(recommend_structure("tag_membership"), "set")
        self.assertEqual(classify_exception(KeyError("event_id")), "missing-field")

    def test_set_membership_normalizes_and_filters_tags(self) -> None:
        events = [
            sentinel_record("evt-1", tags=[" edge ", "temperature", "edge"]),
            sentinel_record("evt-2", "auth.gateway", 5, tags=("security", " alert ")),
            sentinel_record("evt-3", tags=frozenset({"edge", "heartbeat"})),
        ]

        self.assertEqual(normalize_tag_set([" edge ", "edge", "temperature"]), frozenset({"edge", "temperature"}))
        self.assertEqual(unique_tags(events), {"edge", "temperature", "security", "alert", "heartbeat"})
        self.assertEqual([event["event_id"] for event in events_matching_all_tags(events, ["edge"])], ["evt-1", "evt-3"])
        self.assertEqual([event["event_id"] for event in events_matching_all_tags(events, ["edge", "temperature"])], ["evt-1"])
        self.assertEqual([event["event_id"] for event in events_matching_all_tags(events, [])], ["evt-1", "evt-2", "evt-3"])

        with self.assertRaises(TypeError):
            normalize_tag_set(None)
        with self.assertRaises(TypeError):
            normalize_tag_set(["edge", 7])
        with self.assertRaises(ValueError):
            normalize_tag_set(["edge", " "])


class ErrorAndDsaTests(unittest.TestCase):
    def test_validation_and_lookup_errors_are_explicit(self) -> None:
        record = sentinel_record(tags=[" edge "], metadata={"region": "eu"})
        normalized = normalize_event_record(record)
        record["tags"].append("mutated")  # type: ignore[union-attr]
        record["metadata"]["region"] = "changed"  # type: ignore[index]

        self.assertEqual(normalized["tags"], ("edge",))
        self.assertEqual(normalized["metadata"], {"region": "eu"})
        valid = sentinel_record()
        self.assertIs(validate_event_record(valid), valid)
        with self.assertRaises(TypeError):
            validate_event_record(sentinel_record(tags=["edge", 7]))
        with self.assertRaises(TypeError):
            validate_event_record(sentinel_record(severity="5"))
        with self.assertRaises(ValueError):
            validate_event_record(sentinel_record(severity=9))
        self.assertEqual(require_event_field(record, "source"), "sensor.edge-7")
        self.assertEqual(get_event_field(record, "missing", "fallback"), "fallback")

        with self.assertRaises(KeyError):
            require_event_field(record, "missing")
        with self.assertRaises(IndexError):
            get_event_at([record], 2)
        self.assertIsNone(safe_get_event_at([record], 2))

        index = {"evt-1": record}
        self.assertIs(safe_lookup(index, "evt-1"), record)
        self.assertIsNone(find_or_none(index, "missing"))
        self.assertEqual(find_or_default(index, "missing", {}), {})
        self.assertEqual(require_lookup(index, "evt-1"), record)
        self.assertEqual(collect_missing_keys(index, ["evt-1", "evt-2"]), ["evt-2"])
        with self.assertRaisesRegex(KeyError, "evt-2"):
            require_all(index, ["evt-1", "evt-2"])

        self.assertEqual(ensure_hashable_tag(" edge "), "edge")
        self.assertEqual(build_tag_membership(["edge", "edge", "alert"]), {"edge", "alert"})

    def test_indexes_queues_and_registry_preserve_order_and_alias_safety(self) -> None:
        metadata = {"region": "eu-west"}
        records = [
            sentinel_record("evt-1", "sensor.edge-7", 4, tags=["edge", "temperature"], metadata=metadata),
            sentinel_record("evt-2", "auth.gateway", 5, tags=["security", "alert"]),
            sentinel_record("evt-3", "sensor.edge-7", 1, tags=["edge", "heartbeat"]),
        ]

        event_index = EventIndex().build(records)
        metadata["region"] = "changed"
        self.assertEqual(event_index.require("evt-1")["metadata"], {"region": "eu-west"})
        self.assertEqual([event["event_id"] for event in event_index.events_for_source("sensor.edge-7")], ["evt-1", "evt-3"])
        self.assertEqual([event["event_id"] for event in event_index.events_for_severity(5)], ["evt-2"])
        with self.assertRaisesRegex(ValueError, "duplicate event_id"):
            event_index.add(records[0])

        registry = TagRegistry()
        for record in records:
            registry.add_event(record)
        self.assertEqual(registry.event_ids_for_tag("edge"), frozenset({"evt-1", "evt-3"}))
        self.assertTrue(registry.has_tag("evt-2", "alert"))
        self.assertEqual(registry.tags_for_event("evt-1"), frozenset({"edge", "temperature"}))

        queue = SeverityQueue()
        for record in records:
            queue.enqueue(record)
        alerts = queue.drain_min_severity(4)
        self.assertEqual([event["event_id"] for event in alerts], ["evt-1", "evt-2"])
        self.assertEqual(len(queue), 1)


class SolutionSmokeTests(unittest.TestCase):
    def test_entry_mid_and_advanced_solutions_use_current_architecture(self) -> None:
        records = [
            sentinel_record("evt-2001", "sensor.edge-7", 4, tags=["edge", "temperature", "alert"]),
            sentinel_record("evt-2002", "auth.gateway", 5, tags=["security", "alert"]),
            sentinel_record("evt-2003", "sensor.edge-7", 1, tags=["edge", "heartbeat"]),
        ]

        indexes = build_event_indexes(records)
        self.assertEqual(tuple(indexes["by_id"]), ("evt-2001", "evt-2002", "evt-2003"))
        self.assertEqual([event["event_id"] for event in indexes["by_source"]["sensor.edge-7"]], ["evt-2001", "evt-2003"])

        registry = build_tag_registry(records)
        self.assertEqual(registry.event_ids_for_tag("alert"), frozenset({"evt-2001", "evt-2002"}))
        self.assertEqual([event["event_id"] for event in filter_events_by_tags(records, ["edge"])], ["evt-2001", "evt-2003"])

        batch = records + [
            sentinel_record("evt-2002", "sensor.edge-8", 2, tags=["duplicate"]),
            sentinel_record("evt-bad", "sensor.edge-8", 9, tags=["invalid"]),
        ]
        output = ingest_sentinelflow_events(batch)
        self.assertIsInstance(output["index"], EventIndex)
        self.assertIsInstance(output["registry"], TagRegistry)
        self.assertIs(output["tag_registry"], output["registry"])
        self.assertIs(output["events"][0], output["index"].require("evt-2001"))
        self.assertIs(output["events"][0], output["by_id"]["evt-2001"])
        self.assertIs(output["events"][0], output["by_source"]["sensor.edge-7"][0])
        self.assertIs(output["events"][0], output["alerts"][0])
        self.assertEqual(output["event_ids"], ("evt-2001", "evt-2002", "evt-2003"))
        self.assertEqual([event["event_id"] for event in output["alerts"]], ["evt-2001", "evt-2002"])
        self.assertEqual(
            output["summary"],
            {
                "total_events": 3,
                "source_count": 2,
                "tag_count": 5,
                "alert_count": 2,
                "severity_counts": {4: 1, 5: 1, 1: 1},
            },
        )
        self.assertEqual([error["event_id"] for error in output["errors"]], ["evt-2002", "evt-bad"])
        self.assertEqual(output["remaining_queue_size"], 1)

        type_error_batch = [sentinel_record("evt-type", severity="5")]
        type_error_output = ingest_sentinelflow_events(type_error_batch)
        self.assertEqual(type_error_output["errors"][0]["error_type"], "TypeError")


class LabPromptTests(unittest.TestCase):
    def test_lab_files_are_prompt_only(self) -> None:
        lab_dir = Path(__file__).resolve().parents[1] / "lab"
        for name in ("entry_challenge.md", "mid_challenge.md", "advanced_challenge.md"):
            content = (lab_dir / name).read_text(encoding="utf-8")
            self.assertNotIn("def ", content, name)
            self.assertNotIn("class ", content, name)
            self.assertNotIn("```python", content.lower(), name)


if __name__ == "__main__":
    unittest.main()
