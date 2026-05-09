"""ExitStack cleanup ordering."""
from contextlib import ExitStack

def cleanup_order(names):
    log = []
    with ExitStack() as stack:
        for name in names:
            stack.callback(log.append, f"close:{name}")
    return tuple(log)
