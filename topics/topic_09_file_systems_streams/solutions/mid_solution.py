"""Mid solution for Topic 09."""
from topics.topic_09_file_systems_streams.concepts.jsonl_streams import write_jsonl, stream_jsonl
def roundtrip_jsonl(path, events):
    write_jsonl(path, events)
    return tuple(stream_jsonl(path))
