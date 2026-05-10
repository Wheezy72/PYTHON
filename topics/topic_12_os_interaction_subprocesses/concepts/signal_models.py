"""Signal classification helpers."""
def classify_exit(returncode):
    if returncode == 0: return "success"
    if returncode < 0: return "signal"
    return "failure"
