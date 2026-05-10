"""Threaded SentinelFlow ingestion."""
from topics.topic_07_concurrency_threading_multiprocessing.concepts.threading_workers import threaded_map

def normalize_event(event):
    return {**event, "message": event["message"].strip().lower()}

def ingest_threaded(events, max_workers=4):
    return threaded_map(normalize_event, tuple(events), max_workers=max_workers)
