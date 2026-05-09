"""Mid solution for Topic 08."""
from topics.topic_08_asyncio_event_loops_awaitables.concepts.async_queues import fill_queue, drain_queue
async def queue_roundtrip(events):
    return await drain_queue(await fill_queue(events))
