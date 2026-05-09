"""GIL teaching helpers."""
def choose_executor(workload):
    if workload == "io":
        return "threading"
    if workload == "cpu":
        return "multiprocessing"
    raise ValueError("workload must be io or cpu")
