"""Resource leak detection helpers."""
def require_closed(resource):
    if getattr(resource, "open", False):
        raise RuntimeError("resource was not closed")
    return True
