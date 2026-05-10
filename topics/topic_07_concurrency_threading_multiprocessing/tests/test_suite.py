"""Tests for Topic 07."""
import threading, unittest
from pathlib import Path
from topics.topic_07_concurrency_threading_multiprocessing.concepts.gil_overview import choose_executor
from topics.topic_07_concurrency_threading_multiprocessing.concepts.multiprocessing_strategy import chunk_records
from topics.topic_07_concurrency_threading_multiprocessing.concepts.locks_queues import LockedCounter, queue_events
from topics.topic_07_concurrency_threading_multiprocessing.dsa.safe_queue import drain_queue
from topics.topic_07_concurrency_threading_multiprocessing.solutions.entry_solution import normalize_with_threads
from topics.topic_07_concurrency_threading_multiprocessing.solutions.mid_solution import drain_event_queue
from topics.topic_07_concurrency_threading_multiprocessing.solutions.advanced_solution import run_concurrent_ingestion
from topics.topic_07_concurrency_threading_multiprocessing.errors.deadlock_patterns import acquire_with_timeout

def event(event_id="evt-1", message=" HOT "):
    return {"event_id": event_id, "message": message}
class Topic07Tests(unittest.TestCase):
    def test_concepts_and_dsa(self):
        self.assertEqual(choose_executor("io"), "threading"); self.assertEqual(choose_executor("cpu"), "multiprocessing")
        self.assertEqual(chunk_records([1,2,3], 2), ((1,2),(3,)))
        counter = LockedCounter(); self.assertEqual([counter.increment(), counter.increment()], [1,2])
        self.assertEqual([e["event_id"] for e in drain_queue(queue_events([event("a"), event("b")]))], ["a", "b"])
        lock = threading.Lock(); self.assertTrue(acquire_with_timeout(lock)); lock.release()
    def test_solutions(self):
        events = [event("a", " A "), event("b", " B ")]
        self.assertEqual([e["message"] for e in normalize_with_threads(events)], ["a", "b"])
        self.assertEqual([e["event_id"] for e in drain_event_queue(events)], ["a", "b"])
        result = run_concurrent_ingestion(events + [{"bad": True}]); self.assertEqual(result["count"], 2); self.assertEqual(result["errors"][0]["error_type"], "KeyError")
        self.assertEqual([e["message"] for e in run_concurrent_ingestion(events, max_workers=2)["events"]], ["a", "b"])
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_07_concurrency_threading_multiprocessing/lab").glob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            for marker in ("def ", "class ", "import ", "from ", "return ", "```python"):
                self.assertNotIn(marker, text)
if __name__ == "__main__": unittest.main()
