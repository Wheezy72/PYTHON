"""Entry solution for Topic 07."""
from topics.topic_07_concurrency_threading_multiprocessing.dsa.threaded_ingestion import ingest_threaded

def normalize_with_threads(events):
    return ingest_threaded(events)
