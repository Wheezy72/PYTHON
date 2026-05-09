"""Iterator protocol examples."""
class EventStream:
    def __init__(self, events):
        self._events = tuple(events)
        self._index = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index >= len(self._events):
            raise StopIteration
        item = self._events[self._index]
        self._index += 1
        return item
