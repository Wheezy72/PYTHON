"""Incremental frame buffer backed by bytes."""
class ProtocolBuffer:
    def __init__(self): self._buffer = b""
    def feed(self, data): self._buffer += data
    def pop_frames(self):
        frames = []
        while len(self._buffer) >= 4:
            size = int.from_bytes(self._buffer[:4], "big")
            end = 4 + size
            if len(self._buffer) < end: break
            frames.append(self._buffer[:end]); self._buffer = self._buffer[end:]
        return tuple(frames)
    def __len__(self): return len(self._buffer)
