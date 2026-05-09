"""Composition helpers for object pipelines."""
class EventService:
    def __init__(self, store, processors):
        self.store = store
        self.processors = tuple(processors)
    def ingest(self, event):
        current = event
        for processor in self.processors:
            current = processor.process(current)
        self.store.add(current)
        return current
