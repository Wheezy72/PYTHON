"""Sanitization helpers."""
def redact_secrets(record, keys=("password","token","secret")):
    sensitive={k.lower() for k in keys}; return {k:("<redacted>" if k.lower() in sensitive else v) for k,v in record.items()}
