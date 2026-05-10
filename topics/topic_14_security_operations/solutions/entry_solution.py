"""Entry solution for Topic 14."""
from topics.topic_14_security_operations.concepts.hashing import stable_event_hash

def fingerprint_events(events):
    return tuple(stable_event_hash(event) for event in events)
