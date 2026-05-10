"""Timeout-oriented lock acquisition."""
def acquire_with_timeout(lock, timeout=0.1):
    acquired = lock.acquire(timeout=timeout)
    if not acquired:
        raise TimeoutError("could not acquire lock")
    return True
