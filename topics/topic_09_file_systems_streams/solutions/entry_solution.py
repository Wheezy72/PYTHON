"""Entry solution for Topic 09."""
from topics.topic_09_file_systems_streams.concepts.json_io import write_json, read_json
def roundtrip_json(path, data):
    write_json(path, data)
    return read_json(path)
