"""Mid solution for Topic 05."""
from topics.topic_05_iterator_protocol_generators.concepts.lazy_pipelines import lazy_filter, lazy_map

def stream_alerts(events, minimum=4):
    return lazy_filter(events, lambda event: event["severity"] >= minimum)

def normalize_messages(events):
    return lazy_map(events, lambda event: {**event, "message": event["message"].strip().lower()})
