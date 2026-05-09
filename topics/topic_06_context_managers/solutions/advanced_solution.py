"""Advanced solution for Topic 06."""
from contextlib import ExitStack
from topics.topic_06_context_managers.dsa.managed_lock import ManagedFlagLock
from topics.topic_06_context_managers.dsa.transactional_buffer import TransactionalBuffer

def run_managed_ingestion(target, events, audit_log):
    lock = ManagedFlagLock()
    with ExitStack() as stack:
        stack.enter_context(lock)
        tx = stack.enter_context(TransactionalBuffer(target))
        audit_log.append("open")
        stack.callback(audit_log.append, "close")
        for event in events:
            tx.add(event)
    return {"target": tuple(target), "locked": lock.locked, "audit": tuple(audit_log)}
