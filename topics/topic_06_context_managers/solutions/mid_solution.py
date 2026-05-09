"""Mid solution for Topic 06."""
from topics.topic_06_context_managers.dsa.transactional_buffer import TransactionalBuffer

def commit_events(target, events):
    with TransactionalBuffer(target) as tx:
        for event in events:
            tx.add(event)
    return target
