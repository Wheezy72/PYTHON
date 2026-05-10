"""Length-prefixed JSON framing for socket protocols."""
import json

def encode_frame(event):
    payload = json.dumps(event, sort_keys=True, separators=(",", ":")).encode()
    return len(payload).to_bytes(4, "big") + payload

def decode_frame(frame):
    if len(frame) < 4:
        raise ValueError("frame too short")
    size = int.from_bytes(frame[:4], "big")
    payload = frame[4:]
    if len(payload) != size:
        raise ValueError("payload size mismatch")
    return json.loads(payload.decode())
