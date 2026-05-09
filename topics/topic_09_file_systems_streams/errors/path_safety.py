"""Basic path safety."""
from pathlib import Path
def reject_absolute(path):
    path = Path(path)
    if path.is_absolute():
        raise ValueError("absolute paths are not allowed here")
    return path
