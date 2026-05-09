"""ABCs and Protocols for event processors."""
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

class EventProcessor(ABC):
    @abstractmethod
    def process(self, event):
        raise NotImplementedError

@runtime_checkable
class ProcessorProtocol(Protocol):
    def process(self, event): ...

class SeverityCapper(EventProcessor):
    def __init__(self, maximum=5):
        self.maximum = maximum
    def process(self, event):
        copied = dict(event)
        copied["severity"] = min(int(copied["severity"]), self.maximum)
        return copied
