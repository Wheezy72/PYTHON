"""Mid solution for Topic 14."""
from topics.topic_14_security_operations.concepts.sanitization import redact_secrets

def sanitize_event(event):
    copied=dict(event); copied["metadata"]=redact_secrets(dict(event.get("metadata", {}))); return copied
