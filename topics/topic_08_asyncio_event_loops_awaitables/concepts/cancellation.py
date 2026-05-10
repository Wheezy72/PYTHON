"""Cancellation handling."""
import asyncio
async def cancellable_marker():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        return "cancelled"
