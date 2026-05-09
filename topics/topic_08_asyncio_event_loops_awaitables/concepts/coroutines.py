"""Coroutine helpers."""
import asyncio
async def normalize_event(event):
    await asyncio.sleep(0)
    return {**event, "message": event["message"].strip().lower()}
