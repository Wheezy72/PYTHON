"""Benchmark result table."""
class BenchmarkTable:
    def __init__(self): self._rows=[]
    def add(self, name, seconds): self._rows.append({"name":name,"seconds":float(seconds)})
    def fastest(self): return min(self._rows, key=lambda row: row["seconds"])
    def all(self): return tuple(self._rows)
