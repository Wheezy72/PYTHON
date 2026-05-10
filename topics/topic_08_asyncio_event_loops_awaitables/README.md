# Topic 08: Concurrency 2 — Asyncio, Event Loops, Awaitables

Topic 08 adds cooperative SentinelFlow ingestion with coroutines, tasks, async queues, cancellation, and bounded async workers.

## SentinelFlow milestone

Add asyncio ingestion, async queues, cancellation handling, and event-loop-aware processors.

## Complexity overview

| Operation | Time | Space | Structure |
| --- | ---: | ---: | --- |
| Await one coroutine | O(work) | O(1) | Coroutine frame |
| Gather n tasks | O(max task time) ideal | O(n) | Task set |
| Async queue put/get | O(1) | O(n) | FIFO queue |
| Bounded worker run | O(n * work / workers) ideal | O(n) | Queue plus tasks |
