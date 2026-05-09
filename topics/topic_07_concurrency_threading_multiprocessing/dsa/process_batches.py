"""Process-style batch orchestration without requiring spawned processes in tests."""
from topics.topic_07_concurrency_threading_multiprocessing.concepts.multiprocessing_strategy import chunk_records, process_chunk

def ingest_in_chunks(events, transform, chunk_size=2):
    output = []
    for chunk in chunk_records(list(events), chunk_size):
        output.extend(process_chunk(chunk, transform))
    return tuple(output)
