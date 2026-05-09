"""Reusable event stream iterator."""
class ReplayableEventStream:
    def __init__(self, events):
        self._events = tuple(events)
    def __iter__(self):
        return iter(self._events)
    def __len__(self):
        return len(self._events)
