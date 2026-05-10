"""Set-backed UDP event deduplicator."""
class UdpDeduplicator:
    def __init__(self): self._seen = set()
    def accept(self, event_id):
        if event_id in self._seen: return False
        self._seen.add(event_id); return True
    def __len__(self): return len(self._seen)
