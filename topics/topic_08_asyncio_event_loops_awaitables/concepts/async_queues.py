"""Async queue helpers."""
import asyncio
async def fill_queue(events):
    queue = asyncio.Queue()
    for event in events:
        await queue.put(event)
    return queue
async def drain_queue(queue):
    output = []
    while not queue.empty():
        output.append(await queue.get())
    return tuple(output)
