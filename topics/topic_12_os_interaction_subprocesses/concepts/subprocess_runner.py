"""Subprocess execution wrapper."""
import subprocess

def run_command(args, timeout=5):
    if isinstance(args, str): raise TypeError("args must be a sequence, not a shell string")
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
