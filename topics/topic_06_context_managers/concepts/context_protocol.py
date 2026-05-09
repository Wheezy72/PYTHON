"""Context manager protocol examples."""
class EventSession:
    def __init__(self):
        self.open = False
        self.events = []
    def __enter__(self):
        self.open = True
        return self
    def add(self, event):
        if not self.open:
            raise RuntimeError("session is closed")
        self.events.append(event)
    def __exit__(self, exc_type, exc, tb):
        self.open = False
        return False
