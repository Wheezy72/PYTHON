"""Binary event codec using JSON bytes."""
import json
def encode_event(event): return json.dumps(event, sort_keys=True).encode("utf-8")
def decode_event(payload): return json.loads(payload.decode("utf-8"))
