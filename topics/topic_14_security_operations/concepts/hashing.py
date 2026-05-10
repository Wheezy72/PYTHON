"""Hashing helpers."""
import hashlib, json

def stable_event_hash(event):
    payload=json.dumps(event, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()
