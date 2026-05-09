"""Timeout wrappers."""
import asyncio
async def with_timeout(awaitable, timeout):
    return await asyncio.wait_for(awaitable, timeout)
