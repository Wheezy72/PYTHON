"""Iterator object that yields fixed-size batches."""
from topics.topic_05_iterator_protocol_generators.concepts.batching_backpressure import batches
class BatchingIterator:
    def __init__(self, iterable, size):
        self._iterator = iter(batches(iterable, size))
    def __iter__(self):
        return self
    def __next__(self):
        return next(self._iterator)
