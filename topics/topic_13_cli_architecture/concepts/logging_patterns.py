"""Structured CLI log records."""
def log_record(level, message, **fields):
    return {"level":level, "message":message, **fields}
