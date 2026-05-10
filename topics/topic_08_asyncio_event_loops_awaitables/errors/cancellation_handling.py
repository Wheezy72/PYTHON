"""Safe cancellation wrapper."""
import asyncio
async def cancel_and_collect(task):
    task.cancel()
    try:
        return await task
    except asyncio.CancelledError:
        return "cancelled"
