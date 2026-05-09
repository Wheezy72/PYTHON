"""Dictionary-backed processor registry."""
from topics.topic_04_advanced_oop.errors.abstract_contracts import require_processor

class ProcessorRegistry:
    def __init__(self):
        self._processors = {}
    def register(self, name, processor):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be non-empty")
        self._processors[name.strip()] = require_processor(processor)
    def get(self, name):
        return self._processors[name]
    def names(self):
        return tuple(self._processors)
