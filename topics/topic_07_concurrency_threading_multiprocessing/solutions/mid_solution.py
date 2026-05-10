"""Mid solution for Topic 07."""
from topics.topic_07_concurrency_threading_multiprocessing.concepts.locks_queues import queue_events
from topics.topic_07_concurrency_threading_multiprocessing.dsa.safe_queue import drain_queue

def drain_event_queue(events):
    return drain_queue(queue_events(events))
