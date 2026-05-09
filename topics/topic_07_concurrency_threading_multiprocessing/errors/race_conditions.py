"""Race-condition prevention helpers."""
def require_lock(lock):
    if not hasattr(lock, "acquire") or not hasattr(lock, "release"):
        raise TypeError("lock must expose acquire and release")
    return lock
