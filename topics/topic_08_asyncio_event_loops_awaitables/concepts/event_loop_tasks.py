"""Task orchestration."""
import asyncio
async def gather_ordered(coros):
    return tuple(await asyncio.gather(*coros))
