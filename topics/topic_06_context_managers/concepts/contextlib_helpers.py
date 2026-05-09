"""contextlib-based managers."""
from contextlib import contextmanager

@contextmanager
def stage_marker(name, audit_log):
    audit_log.append((name, "enter"))
    try:
        yield name
    finally:
        audit_log.append((name, "exit"))
