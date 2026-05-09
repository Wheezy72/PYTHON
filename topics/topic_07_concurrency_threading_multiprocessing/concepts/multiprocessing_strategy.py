"""Process-friendly chunking helpers."""
def chunk_records(records, size):
    if size <= 0:
        raise ValueError("size must be positive")
    return tuple(tuple(records[index:index + size]) for index in range(0, len(records), size))

def process_chunk(chunk, transform):
    return tuple(transform(record) for record in chunk)
