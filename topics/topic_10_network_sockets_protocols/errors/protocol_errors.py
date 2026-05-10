"""Protocol error taxonomy."""
class ProtocolFrameError(ValueError):
    pass

def require_payload(message):
    if "payload" not in message:
        raise KeyError("payload")
    return message["payload"]
