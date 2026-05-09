# Topic 05: The Iterator Protocol & Generators

Topic 05 makes SentinelFlow stream-oriented. It covers iterator objects, generator functions, generator expressions, lazy pipelines, batching, exhaustion, and memory-efficient processing.

## SentinelFlow milestone

Stream events lazily from generators and iterator-backed pipelines.

## Complexity overview

| Operation | Time | Space | Structure |
| --- | ---: | ---: | --- |
| Next item | O(1) plus source cost | O(1) | Iterator state |
| Lazy filter/map | O(n * stage cost) | O(1) extra | Generator frame |
| Batch size b | O(b) per batch | O(b) | Tuple buffer |
| Replayable materialization | O(n) | O(n) | List cache |

## Tests

```bash
python -m unittest discover -s topics/topic_05_iterator_protocol_generators/tests -p 'test_suite.py'
```
