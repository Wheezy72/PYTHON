"""Replay helpers."""
def replay_window(events, limit):
    if limit < 0: raise ValueError("limit must be non-negative")
    return tuple(events)[-limit:] if limit else tuple()
