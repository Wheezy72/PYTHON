"""Simple fixed-window rate limiting."""
def within_limit(count, limit):
    if limit <= 0: raise ValueError("limit must be positive")
    return count < limit
