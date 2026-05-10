"""Protocol message validation."""
VALID_TYPES = {"event", "ack", "error"}

def validate_message(message):
    if not isinstance(message, dict):
        raise TypeError("message must be a dict")
    if message.get("type") not in VALID_TYPES:
        raise ValueError("unsupported message type")
    return message
