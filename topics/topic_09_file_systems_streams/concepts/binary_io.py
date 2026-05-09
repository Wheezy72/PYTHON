"""Binary payload helpers."""
def encode_payload(text):
    return text.encode("utf-8")
def decode_payload(payload):
    return payload.decode("utf-8")
