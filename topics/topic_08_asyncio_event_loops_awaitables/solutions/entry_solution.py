"""Entry solution for Topic 08."""
from topics.topic_08_asyncio_event_loops_awaitables.concepts.coroutines import normalize_event
async def normalize_one(event):
    return await normalize_event(event)
