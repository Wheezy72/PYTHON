"""Retry validation."""
def should_retry(status, attempt, max_attempts):
    return status in {429, 500, 502, 503, 504} and attempt < max_attempts
