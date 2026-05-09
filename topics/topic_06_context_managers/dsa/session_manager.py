"""SentinelFlow session manager."""
from topics.topic_06_context_managers.dsa.transactional_buffer import TransactionalBuffer
class SentinelSession:
    def __init__(self):
        self.events = []
    def transaction(self):
        return TransactionalBuffer(self.events)
