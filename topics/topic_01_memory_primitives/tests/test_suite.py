"""Tests for Topic 01: Memory & Primitives."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError

from topics.topic_01_memory_primitives.concepts.copy_reference import (
    deep_copy_metadata,
    reference_copy_metadata,
    shallow_copy_metadata,
)
from topics.topic_01_memory_primitives.concepts.identity_equality import identity_report
from topics.topic_01_memory_primitives.concepts.interning import interning_observation
from topics.topic_01_memory_primitives.concepts.memory_measurement import deep_size, shallow_size
from topics.topic_01_memory_primitives.concepts.mutability_aliasing import (
    append_tag_copy,
    append_tag_in_place,
)
from topics.topic_01_memory_primitives.concepts.primitive_object_model import (
    build_event_tuple,
    event_tuple_to_record,
)
from topics.topic_01_memory_primitives.dsa.memory_inspector import (
    compare_event_memory,
    event_memory_profile,
)
from topics.topic_01_memory_primitives.dsa.primitive_event import PrimitiveEvent
from topics.topic_01_memory_primitives.dsa.tag_index import build_tag_index, events_with_tag
from topics.topic_01_memory_primitives.errors.aliasing_shared_state import (
    safe_attach_tag,
    unsafe_attach_tag,
)
from topics.topic_01_memory_primitives.errors.event_validation import (
    normalize_event_record,
    validate_event_record,
)
from topics.topic_01_memory_primitives.errors.immutable_type_errors import (
    attempt_tuple_tag_mutation,
    safe_extend_tuple_tags,
)
from topics.topic_01_memory_primitives.solutions.advanced_solution import (
    profile_and_index_events,
)
from topics.topic_01_memory_primitives.solutions.entry_solution import (
    make_event_identity_snapshot,
)
from topics.topic_01_memory_primitives.solutions.mid_solution import (
    add_tag_without_aliasing,
    prepare_event,
)


def sentinel_record(
    event_id: str = "evt-1001",
    source: str = "sensor.edge-7",
    severity: int = 3,
    message: str = "temperature threshold crossed",
    tags: list[str] | tuple[str, ...] | None = None,
    metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "event_id": event_id,
        "source": source,
        "severity": severity,
        "message": message,
        "tags": ["edge", "temperature"] if tags is None else tags,
        "metadata": {"region": "eu-west", "device_id": "edge-7"} if metadata is None else metadata,
    }


class ConceptHelperTests(unittest.TestCase):
    def test_identity_report_distinguishes_identity_and_equality(self) -> None:
        left = ["edge", "temperature"]
        right = ["edge", "temperature"]
        report = identity_report(left, right)
        self.assertFalse(report["same_identity"])
        self.assertTrue(report["same_value"])
        self.assertEqual(report["left_type"], "list")
        self.assertEqual(report["right_type"], "list")

    def test_mutability_aliasing_helpers(self) -> None:
        tags = ["edge"]
        alias = tags
        result = append_tag_in_place(tags, "hot")
        self.assertIs(result, tags)
        self.assertEqual(alias, ["edge", "hot"])

        copied = append_tag_copy(tags, "safe")
        self.assertEqual(copied, ("edge", "hot", "safe"))
        self.assertEqual(tags, ["edge", "hot"])

    def test_event_tuple_helpers(self) -> None:
        event = build_event_tuple("evt-1", "sensor", 2, "ok")
        self.assertEqual(event[0], "evt-1")
        self.assertEqual(
            event_tuple_to_record(event),
            {"event_id": "evt-1", "source": "sensor", "severity": 2, "message": "ok"},
        )

    def test_copy_reference_helpers(self) -> None:
        metadata = {"device": {"id": "edge-7"}, "count": 1}
        reference = reference_copy_metadata(metadata)
        shallow = shallow_copy_metadata(metadata)
        deep = deep_copy_metadata(metadata)

        self.assertIs(reference, metadata)
        self.assertIsNot(shallow, metadata)
        self.assertIs(shallow["device"], metadata["device"])
        self.assertIsNot(deep, metadata)
        self.assertIsNot(deep["device"], metadata["device"])

    def test_memory_size_handles_cycles(self) -> None:
        cycle: list[object] = []
        cycle.append(cycle)
        self.assertGreater(shallow_size(cycle), 0)
        self.assertGreater(deep_size(cycle), 0)
        self.assertLess(deep_size(cycle), 10_000)

    def test_interning_observation_basics(self) -> None:
        value = "sentinel-flow-tag"
        observation = interning_observation(value)
        self.assertTrue(observation["equal"])
        self.assertIsInstance(observation["interned"], str)
        self.assertIn("same_identity_after_intern", observation)


class ErrorHandlingTests(unittest.TestCase):
    def test_tuple_mutation_raises_type_error_and_safe_extension_returns_new_tuple(self) -> None:
        with self.assertRaises(TypeError):
            attempt_tuple_tag_mutation(("edge",), "hot")
        original = ("edge",)
        extended = safe_extend_tuple_tags(original, "hot")
        self.assertEqual(extended, ("edge", "hot"))
        self.assertEqual(original, ("edge",))

    def test_validation_key_error_and_value_errors(self) -> None:
        missing = sentinel_record()
        del missing["message"]
        with self.assertRaises(KeyError):
            validate_event_record(missing)

        for invalid in (
            sentinel_record(severity=0),
            sentinel_record(message=""),
            sentinel_record(tags=["edge", 3]),
            sentinel_record(metadata=[]),  # type: ignore[arg-type]
        ):
            with self.assertRaises(ValueError):
                validate_event_record(invalid)

    def test_normalize_returns_new_aliasing_safe_record(self) -> None:
        record = sentinel_record()
        normalized = normalize_event_record(record)
        self.assertIsNot(normalized, record)
        self.assertEqual(normalized["tags"], ("edge", "temperature"))
        self.assertIsNot(normalized["metadata"], record["metadata"])
        record["tags"].append("mutated")  # type: ignore[union-attr]
        self.assertEqual(normalized["tags"], ("edge", "temperature"))

    def test_safe_vs_unsafe_aliasing_behavior(self) -> None:
        record = sentinel_record(tags=["edge"])
        unsafe_result = unsafe_attach_tag(record, "unsafe")
        self.assertIs(unsafe_result, record)
        self.assertEqual(record["tags"], ["edge", "unsafe"])

        safe_result = safe_attach_tag(record, "safe")
        self.assertIsNot(safe_result, record)
        self.assertEqual(safe_result["tags"], ("edge", "unsafe", "safe"))
        self.assertEqual(record["tags"], ["edge", "unsafe"])
        self.assertIsNot(safe_result["metadata"], record["metadata"])


class DsaHelperTests(unittest.TestCase):
    def test_primitive_event_normalization_and_immutability(self) -> None:
        metadata = {"region": "eu-west"}
        event = PrimitiveEvent("evt-1", "sensor", 2, "ok", ["edge"], metadata)  # type: ignore[arg-type]
        self.assertEqual(event.tags, ("edge",))
        self.assertIsNot(event.metadata, metadata)
        metadata["region"] = "changed"
        self.assertEqual(event.metadata["region"], "eu-west")
        with self.assertRaises(FrozenInstanceError):
            event.severity = 5  # type: ignore[misc]
        with self.assertRaises(TypeError):
            event.metadata["region"] = "changed-again"  # type: ignore[index]

        record = event.to_record()
        self.assertIsInstance(record["metadata"], dict)
        record["metadata"]["region"] = "record-only-change"  # type: ignore[index]
        self.assertEqual(event.metadata["region"], "eu-west")

    def test_primitive_event_with_tag_and_record_roundtrip(self) -> None:
        event = PrimitiveEvent.from_record(sentinel_record())
        tagged = event.with_tag("alert")
        self.assertEqual(event.tags, ("edge", "temperature"))
        self.assertEqual(tagged.tags, ("edge", "temperature", "alert"))
        with self.assertRaises(ValueError):
            event.with_tag("")

        record = tagged.to_record()
        self.assertEqual(record["tags"], ("edge", "temperature", "alert"))
        self.assertIsNot(record["metadata"], tagged.metadata)
        roundtrip = PrimitiveEvent.from_record(record)
        self.assertEqual(roundtrip, tagged)

    def test_tag_index_and_lookup(self) -> None:
        events = (
            PrimitiveEvent.from_record(sentinel_record("evt-1", tags=["edge", "temperature"])),
            PrimitiveEvent.from_record(sentinel_record("evt-2", tags=["edge", "security"])),
        )
        index = build_tag_index(events)
        self.assertEqual(events_with_tag(index, "edge"), ("evt-1", "evt-2"))
        self.assertEqual(events_with_tag(index, "security"), ("evt-2",))
        self.assertEqual(events_with_tag(index, "missing"), ())

    def test_memory_inspector_summary(self) -> None:
        events = (
            PrimitiveEvent.from_record(sentinel_record("evt-1")),
            PrimitiveEvent.from_record(sentinel_record("evt-2", tags=["edge"])),
        )
        profile = event_memory_profile(events[0])
        self.assertGreater(profile["record_shallow_size"], 0)
        self.assertGreaterEqual(profile["record_deep_size"], profile["record_shallow_size"])

        summary = compare_event_memory(events)
        self.assertEqual(summary["count"], 2)
        self.assertGreater(summary["total_deep_size"], 0)
        self.assertGreater(summary["average_deep_size"], 0)
        self.assertGreater(summary["max_deep_size"], 0)
        self.assertEqual(compare_event_memory(()), {"count": 0, "total_deep_size": 0, "average_deep_size": 0.0, "max_deep_size": 0})


class SolutionTests(unittest.TestCase):
    def test_entry_solution_snapshot(self) -> None:
        snapshot = make_event_identity_snapshot("evt-1", "sensor", 2, "ok")
        self.assertEqual(snapshot["left_event"], snapshot["right_event"])
        self.assertTrue(snapshot["identity_report"]["same_value"])  # type: ignore[index]
        self.assertEqual(snapshot["record"]["event_id"], "evt-1")  # type: ignore[index]

    def test_mid_solution_prepares_and_adds_tag_without_aliasing(self) -> None:
        record = sentinel_record(tags=["edge"])
        prepared = prepare_event(record)
        self.assertEqual(prepared["tags"], ("edge",))
        tagged = add_tag_without_aliasing(prepared, "reviewed")
        self.assertEqual(tagged["tags"], ("edge", "reviewed"))
        self.assertEqual(prepared["tags"], ("edge",))

    def test_advanced_solution_profiles_and_indexes(self) -> None:
        output = profile_and_index_events([
            sentinel_record("evt-1", tags=["edge", "temperature"]),
            sentinel_record("evt-2", tags=["edge", "heartbeat"]),
        ])
        self.assertEqual(len(output["events"]), 2)  # type: ignore[arg-type]
        self.assertEqual(output["tag_index"]["edge"], ["evt-1", "evt-2"])  # type: ignore[index]
        self.assertEqual(output["memory_summary"]["count"], 2)  # type: ignore[index]


class IntegrationSmokeTests(unittest.TestCase):
    def test_realistic_sentinelflow_pipeline(self) -> None:
        records = [
            sentinel_record(
                "evt-2001",
                "sensor.edge-7",
                4,
                "temperature threshold crossed",
                ["edge", "temperature", "alert"],
                {"region": "eu-west", "device_id": "edge-7", "reading": 83.2},
            ),
            sentinel_record(
                "evt-2002",
                "auth.gateway",
                5,
                "failed login burst detected",
                ["security", "alert"],
                {"region": "us-east", "attempts": 19},
            ),
            sentinel_record(
                "evt-2003",
                "sensor.edge-7",
                1,
                "heartbeat received",
                ["edge", "heartbeat"],
                {"region": "eu-west", "latency_ms": 12},
            ),
        ]
        original_first_tags = records[0]["tags"]
        output = profile_and_index_events(records)

        events = output["events"]
        index = output["tag_index"]
        memory_summary = output["memory_summary"]

        self.assertEqual(memory_summary["count"], 3)  # type: ignore[index]
        self.assertGreater(memory_summary["total_deep_size"], 0)  # type: ignore[index]
        self.assertEqual(index["alert"], ["evt-2001", "evt-2002"])  # type: ignore[index]
        self.assertEqual(index["edge"], ["evt-2001", "evt-2003"])  # type: ignore[index]
        self.assertEqual(original_first_tags, ["edge", "temperature", "alert"])
        self.assertEqual(events[0].tags, ("edge", "temperature", "alert"))  # type: ignore[index]

        records[0]["tags"].append("mutated-after-pipeline")  # type: ignore[union-attr]
        records[0]["metadata"]["region"] = "changed"  # type: ignore[index]
        self.assertEqual(events[0].tags, ("edge", "temperature", "alert"))  # type: ignore[index]
        self.assertEqual(events[0].metadata["region"], "eu-west")  # type: ignore[index]


if __name__ == "__main__":
    unittest.main()
