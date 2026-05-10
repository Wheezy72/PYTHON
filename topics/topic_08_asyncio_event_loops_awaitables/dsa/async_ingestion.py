"""Async SentinelFlow ingestion."""
import asyncio
from topics.topic_08_asyncio_event_loops_awaitables.concepts.coroutines import normalize_event
async def ingest_async(events):
    return tuple(await asyncio.gather(*(normalize_event(event) for event in events)))
