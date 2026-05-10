"""Advanced solution for Topic 14."""
from topics.topic_14_security_operations.concepts.hashing import stable_event_hash
from topics.topic_14_security_operations.concepts.signing import sign_message, verify_signature
from topics.topic_14_security_operations.errors.security_errors import require_secret

def sign_events(events, secret):
    require_secret(secret); signed=[]
    for event in events:
        digest=stable_event_hash(event); signed.append({"event":event, "digest":digest, "signature":sign_message(secret, digest)})
    return tuple(signed)

def verify_signed_event(signed, secret):
    return verify_signature(secret, signed["digest"], signed["signature"])
