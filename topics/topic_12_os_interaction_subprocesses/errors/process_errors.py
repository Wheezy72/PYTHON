"""Process error helpers."""
def require_success(result):
    if result.returncode != 0: raise RuntimeError(result.stderr.strip() or f"exit {result.returncode}")
    return result
