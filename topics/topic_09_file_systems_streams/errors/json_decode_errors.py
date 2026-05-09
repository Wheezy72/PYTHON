"""JSON decode wrapper."""
import json
def parse_json_line(line):
    try:
        return json.loads(line)
    except json.JSONDecodeError as exc:
        raise ValueError("invalid json line") from exc
