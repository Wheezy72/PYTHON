"""JSONL event log abstraction."""
from topics.topic_09_file_systems_streams.concepts.jsonl_streams import write_jsonl, stream_jsonl
class EventLogFile:
    def __init__(self, path): self.path = path
    def write(self, events): write_jsonl(self.path, events); return self
    def stream(self): return stream_jsonl(self.path)
    def read_all(self): return tuple(self.stream())
