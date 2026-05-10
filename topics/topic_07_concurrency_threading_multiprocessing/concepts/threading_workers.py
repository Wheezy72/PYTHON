"""ThreadPoolExecutor helpers."""
from concurrent.futures import ThreadPoolExecutor

def threaded_map(function, records, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return tuple(pool.map(function, records))
