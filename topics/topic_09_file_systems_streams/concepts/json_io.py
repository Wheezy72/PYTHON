"""JSON file helpers."""
import json
from topics.topic_09_file_systems_streams.concepts.pathlib_files import ensure_parent
def write_json(path, data):
    path = ensure_parent(path); path.write_text(json.dumps(data, sort_keys=True), encoding="utf-8"); return path
def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
