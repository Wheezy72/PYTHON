"""Performance guardrails."""
def require_positive_limit(limit):
    if not isinstance(limit, int): raise TypeError("limit must be an int")
    if limit <= 0: raise ValueError("limit must be positive")
    return limit
