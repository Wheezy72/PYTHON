"""Dictionary-backed response cache."""
class ResponseCache:
    def __init__(self): self._cache={}
    def get_or_set(self, key, factory):
        if key not in self._cache: self._cache[key]=factory()
        return self._cache[key]
    def __len__(self): return len(self._cache)
