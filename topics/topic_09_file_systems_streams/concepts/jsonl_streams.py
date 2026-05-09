"""JSONL streaming helpers."""
import json
from topics.topic_09_file_systems_streams.concepts.pathlib_files import ensure_parent
def write_jsonl(path, events):
    path = ensure_parent(path)
    with path.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
    return path
def stream_jsonl(path):
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)
