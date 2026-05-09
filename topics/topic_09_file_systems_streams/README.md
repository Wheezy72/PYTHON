# Topic 09: File Systems & Streams

Topic 09 persists and replays SentinelFlow events using pathlib, JSON, JSONL, binary payloads, and buffered streams.

## SentinelFlow milestone

Persist and replay events from JSON, JSONL, binary files, and buffered streams.

## Complexity overview

| Operation | Time | Space | Structure |
| --- | ---: | ---: | --- |
| Write n JSONL events | O(n * encode) | O(1) streaming | Text file buffer |
| Read JSONL eagerly | O(n) | O(n) | List of dicts |
| Stream JSONL lazily | O(n) total | O(1) extra | File iterator |
| Binary encode payload | O(b) | O(b) | Bytes buffer |
