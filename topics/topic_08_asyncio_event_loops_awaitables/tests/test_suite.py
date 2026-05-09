"""Tests for Topic 08."""
import asyncio, unittest
from pathlib import Path
from topics.topic_08_asyncio_event_loops_awaitables.concepts.coroutines import normalize_event
from topics.topic_08_asyncio_event_loops_awaitables.concepts.event_loop_tasks import gather_ordered
from topics.topic_08_asyncio_event_loops_awaitables.concepts.async_queues import fill_queue, drain_queue
from topics.topic_08_asyncio_event_loops_awaitables.dsa.async_pipeline import AsyncPipeline
from topics.topic_08_asyncio_event_loops_awaitables.dsa.async_ingestion import ingest_async
from topics.topic_08_asyncio_event_loops_awaitables.errors.awaitable_type_errors import ensure_awaitable
from topics.topic_08_asyncio_event_loops_awaitables.solutions.mid_solution import queue_roundtrip
from topics.topic_08_asyncio_event_loops_awaitables.solutions.advanced_solution import run_async_ingestion

def event(event_id="evt-1", message=" HOT "):
    return {"event_id": event_id, "message": message}
class Topic08Tests(unittest.IsolatedAsyncioTestCase):
    async def test_async_concepts_and_dsa(self):
        self.assertEqual((await normalize_event(event()))["message"], "hot")
        self.assertEqual(await gather_ordered([normalize_event(event("a")), normalize_event(event("b"))]), ({"event_id":"a","message":"hot"},{"event_id":"b","message":"hot"}))
        self.assertEqual([e["event_id"] for e in await drain_queue(await fill_queue([event("a"), event("b")]))], ["a", "b"])
        awaitable = normalize_event(event())
        ensure_awaitable(awaitable)
        await awaitable
        with self.assertRaises(TypeError): ensure_awaitable(3)
        pipe = AsyncPipeline().then(normalize_event); self.assertEqual((await pipe.run_one(event()))["message"], "hot")
        self.assertEqual([e["message"] for e in await ingest_async([event("a"), event("b")])], ["hot", "hot"])
    async def test_solutions(self):
        events = [event("a", " A "), event("b", " B ")]
        self.assertEqual([e["event_id"] for e in await queue_roundtrip(events)], ["a", "b"])
        result = await run_async_ingestion(events, 1); self.assertEqual(result["count"], 2); self.assertEqual(result["events"][0]["message"], "a")
        with self.assertRaises(ValueError):
            await run_async_ingestion(events, 0)
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_08_asyncio_event_loops_awaitables/lab").glob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            for marker in ("def ", "class ", "import ", "from ", "return ", "```python"):
                self.assertNotIn(marker, text)
if __name__ == "__main__": unittest.main()
