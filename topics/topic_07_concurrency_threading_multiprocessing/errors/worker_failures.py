"""Worker error collection."""
def collect_worker_result(function, record):
    try:
        return {"ok": True, "value": function(record)}
    except Exception as exc:
        return {"ok": False, "error_type": type(exc).__name__, "error": str(exc)}
