"""HTTP status classification."""
def classify_status(status):
    if status < 400: return "ok"
    if status == 429: return "rate-limited"
    if 400 <= status < 500: return "client-error"
    return "server-error"
