"""Advanced solution for Topic 08."""
from topics.topic_08_asyncio_event_loops_awaitables.concepts.coroutines import normalize_event
from topics.topic_08_asyncio_event_loops_awaitables.dsa.bounded_workers import bounded_map
async def run_async_ingestion(events, limit=2):
    accepted = await bounded_map(events, normalize_event, limit)
    return {"events": accepted, "count": len(accepted)}
