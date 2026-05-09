"""Simple lock-like context manager for teaching."""
class ManagedFlagLock:
    def __init__(self):
        self.locked = False
    def __enter__(self):
        if self.locked:
            raise RuntimeError("lock already held")
        self.locked = True
        return self
    def __exit__(self, exc_type, exc, tb):
        self.locked = False
        return False
