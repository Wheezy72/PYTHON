"""Entry solution for Topic 05."""
from topics.topic_05_iterator_protocol_generators.concepts.iterator_protocol import EventStream

def collect_event_ids(events):
    return tuple(event["event_id"] for event in EventStream(events))
