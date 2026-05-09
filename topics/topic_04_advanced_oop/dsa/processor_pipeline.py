"""Polymorphic processor pipeline."""
from topics.topic_04_advanced_oop.errors.abstract_contracts import require_processor

class ProcessorPipeline:
    def __init__(self, processors=()):
        self._processors = tuple(require_processor(p) for p in processors)
    def run(self, event):
        current = event
        for processor in self._processors:
            current = processor.process(current)
        return current
    def then(self, processor):
        return ProcessorPipeline((*self._processors, processor))
    def __len__(self):
        return len(self._processors)
