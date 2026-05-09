"""Entry solution for Topic 06."""
from topics.topic_06_context_managers.concepts.context_protocol import EventSession

def collect_with_session(events):
    with EventSession() as session:
        for event in events:
            session.add(event)
        collected = tuple(session.events)
    return collected, session.open
