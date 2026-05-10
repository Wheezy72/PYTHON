"""Append-only audit log."""
class AuditLog:
    def __init__(self): self._entries=[]
    def append(self, action, subject): self._entries.append({"action":action,"subject":subject})
    def all(self): return tuple(self._entries)
