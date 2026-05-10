"""List-backed process history."""
class ProcessHistory:
    def __init__(self): self._entries=[]
    def add(self, args, returncode): self._entries.append({"args":tuple(args),"returncode":returncode})
    def failures(self): return tuple(e for e in self._entries if e["returncode"] != 0)
    def __len__(self): return len(self._entries)
