"""Contract checks for OOP processors."""
def require_processor(obj):
    if not hasattr(obj, "process") or not callable(obj.process):
        raise TypeError("processor must expose a callable process(event)")
    return obj
