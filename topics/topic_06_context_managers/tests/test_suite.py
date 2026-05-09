"""Tests for Topic 06."""
import unittest
from pathlib import Path
from topics.topic_06_context_managers.concepts.context_protocol import EventSession
from topics.topic_06_context_managers.concepts.contextlib_helpers import stage_marker
from topics.topic_06_context_managers.concepts.exception_propagation import SuppressValueError
from topics.topic_06_context_managers.concepts.exit_stack_usage import cleanup_order
from topics.topic_06_context_managers.dsa.managed_lock import ManagedFlagLock
from topics.topic_06_context_managers.dsa.session_manager import SentinelSession
from topics.topic_06_context_managers.dsa.transactional_buffer import TransactionalBuffer
from topics.topic_06_context_managers.errors.resource_leaks import require_closed
from topics.topic_06_context_managers.errors.suppression_mistakes import should_suppress
from topics.topic_06_context_managers.solutions.entry_solution import collect_with_session
from topics.topic_06_context_managers.solutions.mid_solution import commit_events
from topics.topic_06_context_managers.solutions.advanced_solution import run_managed_ingestion

def event(event_id="evt-1"):
    return {"event_id": event_id}

class Topic06Tests(unittest.TestCase):
    def test_context_concepts_and_errors(self):
        with EventSession() as session:
            session.add(event())
            self.assertTrue(session.open)
        self.assertFalse(session.open); self.assertTrue(require_closed(session))
        log = []
        with stage_marker("parse", log): self.assertEqual(log, [("parse", "enter")])
        self.assertEqual(log, [("parse", "enter"), ("parse", "exit")])
        with SuppressValueError(): raise ValueError("ok")
        self.assertTrue(should_suppress(ValueError, (ValueError,)))
        self.assertEqual(cleanup_order(["a", "b"]), ("close:b", "close:a"))
    def test_dsa_and_solutions(self):
        target = []
        with TransactionalBuffer(target) as tx: tx.add(event("a")); tx.add(event("b"))
        self.assertEqual([e["event_id"] for e in target], ["a", "b"])
        with self.assertRaises(RuntimeError):
            with TransactionalBuffer(target) as tx:
                tx.add(event("c")); raise RuntimeError("rollback")
        self.assertEqual([e["event_id"] for e in target], ["a", "b"])
        lock = ManagedFlagLock()
        with lock: self.assertTrue(lock.locked)
        self.assertFalse(lock.locked)
        session = SentinelSession(); commit_events(session.events, [event("x")]); self.assertEqual(session.events[0]["event_id"], "x")
        collected, open_state = collect_with_session([event("s")]); self.assertEqual(collected[0]["event_id"], "s"); self.assertFalse(open_state)
        audit = []; result = run_managed_ingestion([], [event("z")], audit); self.assertEqual(result["target"][0]["event_id"], "z"); self.assertFalse(result["locked"]); self.assertEqual(result["audit"], ("open", "close"))
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_06_context_managers/lab").glob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            for marker in ("def ", "class ", "import ", "from ", "return ", "```python"):
                self.assertNotIn(marker, text)
if __name__ == "__main__": unittest.main()
