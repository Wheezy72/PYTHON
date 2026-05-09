"""Tests for Topic 05."""
import unittest
from pathlib import Path
from topics.topic_05_iterator_protocol_generators.concepts.iterator_protocol import EventStream
from topics.topic_05_iterator_protocol_generators.concepts.generator_basics import chain_sources, event_ids
from topics.topic_05_iterator_protocol_generators.concepts.generator_expressions import high_severity_ids
from topics.topic_05_iterator_protocol_generators.concepts.batching_backpressure import batches
from topics.topic_05_iterator_protocol_generators.dsa.event_stream import ReplayableEventStream
from topics.topic_05_iterator_protocol_generators.dsa.lazy_pipeline import LazyPipeline
from topics.topic_05_iterator_protocol_generators.dsa.batching_iterator import BatchingIterator
from topics.topic_05_iterator_protocol_generators.errors.non_iterable_type_error import ensure_iterable
from topics.topic_05_iterator_protocol_generators.errors.stop_iteration_patterns import consume_one
from topics.topic_05_iterator_protocol_generators.solutions.entry_solution import collect_event_ids
from topics.topic_05_iterator_protocol_generators.solutions.mid_solution import normalize_messages, stream_alerts
from topics.topic_05_iterator_protocol_generators.solutions.advanced_solution import run_streaming_ingestion

def event(event_id="evt-1", severity=3, message=" HOT "):
    return {"event_id": event_id, "severity": severity, "message": message}

class Topic05Tests(unittest.TestCase):
    def test_iterators_generators_and_errors(self):
        events = [event("a", 1), event("b", 5), event("c", 4)]
        stream = EventStream(events); self.assertIs(iter(stream), stream); self.assertEqual([e["event_id"] for e in stream], ["a", "b", "c"])
        self.assertEqual(tuple(event_ids(events)), ("a", "b", "c"))
        self.assertEqual([e["event_id"] for e in chain_sources(events[:1], events[1:])], ["a", "b", "c"])
        self.assertEqual(tuple(high_severity_ids(events, 4)), ("b", "c"))
        self.assertEqual(tuple(len(batch) for batch in batches(events, 2)), (2, 1))
        with self.assertRaises(ValueError): tuple(batches(events, 0))
        with self.assertRaises(TypeError): ensure_iterable(12)
        iterator = iter([]); self.assertEqual(consume_one(iterator, "empty"), "empty")
    def test_dsa_and_solutions(self):
        events = [event("a", 1, " A "), event("b", 5, " B "), event("c", 4, " C ")]
        replay = ReplayableEventStream(events); self.assertEqual(len(replay), 3); self.assertEqual(len(tuple(replay)), 3); self.assertEqual(len(tuple(replay)), 3)
        pipeline = LazyPipeline().then(lambda s: (e for e in s if e["severity"] >= 4))
        self.assertEqual([e["event_id"] for e in pipeline.run(events)], ["b", "c"])
        self.assertEqual([len(batch) for batch in BatchingIterator(events, 2)], [2, 1])
        self.assertEqual(collect_event_ids(events), ("a", "b", "c"))
        self.assertEqual([e["message"] for e in normalize_messages(events)], ["a", "b", "c"])
        self.assertEqual([e["event_id"] for e in stream_alerts(events, 4)], ["b", "c"])
        result = run_streaming_ingestion(events, 4, 1); self.assertEqual([[e["event_id"] for e in batch] for batch in result["batches"]], [["b"], ["c"]])
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_05_iterator_protocol_generators/lab").glob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            for marker in ("def ", "class ", "import ", "from ", "return ", "```python"):
                self.assertNotIn(marker, text)
if __name__ == "__main__": unittest.main()
