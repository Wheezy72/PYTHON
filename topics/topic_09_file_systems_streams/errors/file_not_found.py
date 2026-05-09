"""File existence guards."""
from pathlib import Path
def require_file(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    return path
