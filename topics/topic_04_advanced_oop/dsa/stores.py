"""Storage abstractions backed by linear structures."""
from abc import ABC, abstractmethod

class EventStore(ABC):
    @abstractmethod
    def add(self, event): ...
    @abstractmethod
    def all(self): ...

class InMemoryEventStore(EventStore):
    def __init__(self):
        self._events = []
    def add(self, event):
        self._events.append(event)
        return event
    def all(self):
        return tuple(self._events)
    def by_source(self):
        groups = {}
        for event in self._events:
            groups.setdefault(event["source"], []).append(event)
        return {key: tuple(value) for key, value in groups.items()}
