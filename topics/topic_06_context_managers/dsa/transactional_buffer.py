"""Transactional event buffer."""
class TransactionalBuffer:
    def __init__(self, target):
        self.target = target
        self._buffer = []
    def __enter__(self):
        return self
    def add(self, event):
        self._buffer.append(event)
    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.target.extend(self._buffer)
        self._buffer.clear()
        return False
