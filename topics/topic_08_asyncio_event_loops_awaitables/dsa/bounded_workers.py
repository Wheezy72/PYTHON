"""Bounded async worker helpers."""
import asyncio
async def bounded_map(events, worker, limit=2):
    if limit <= 0:
        raise ValueError("limit must be positive")
    semaphore = asyncio.Semaphore(limit)
    async def run(event):
        async with semaphore:
            return await worker(event)
    return tuple(await asyncio.gather(*(run(event) for event in events)))
