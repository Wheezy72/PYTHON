"""Timeout validation helpers."""
def normalize_timeout(seconds):
    if not isinstance(seconds, (int, float)):
        raise TypeError("timeout must be numeric")
    if seconds <= 0:
        raise ValueError("timeout must be positive")
    return float(seconds)
