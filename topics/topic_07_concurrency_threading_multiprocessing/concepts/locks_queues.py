"""Locks and queues for safe shared state."""
from queue import Queue
from threading import Lock

class LockedCounter:
    def __init__(self):
        self._value = 0
        self._lock = Lock()
    def increment(self):
        with self._lock:
            self._value += 1
            return self._value
    @property
    def value(self):
        return self._value

def queue_events(records):
    queue = Queue()
    for record in records:
        queue.put(record)
    return queue
