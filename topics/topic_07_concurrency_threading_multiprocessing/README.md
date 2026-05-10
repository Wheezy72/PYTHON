# Topic 07: Concurrency 1 — GIL, Threading vs Multiprocessing

Topic 07 introduces SentinelFlow worker execution with threads, process-friendly chunking, locks, and queues.

## SentinelFlow milestone

Add threaded and multiprocessing ingestion workers; compare GIL effects for CPU-bound and I/O-bound work.

## Complexity overview

| Operation | Time | Space | Structure |
| --- | ---: | ---: | --- |
| Threaded map | O(n * work / workers) ideal | O(n) | Thread pool futures |
| Queue drain | O(n) | O(n) | FIFO queue |
| Locked counter update | O(1) | O(1) | Mutex-protected integer |
| Chunk records | O(n) | O(n) | List chunks |

## Tests

```bash
python -m unittest discover -s topics/topic_07_concurrency_threading_multiprocessing/tests -p 'test_suite.py'
```
