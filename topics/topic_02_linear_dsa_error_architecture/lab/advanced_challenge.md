# Advanced Challenge: SentinelFlow In-Memory Ingestion

Combine linear structures, hash-backed indexes, a FIFO queue, and error taxonomy into one ingestion milestone.

## Goal

Build an in-memory SentinelFlow ingestion pipeline that accepts event records and returns:

- normalized events;
- an event index by id, source, and severity;
- a tag registry;
- high-severity alerts drained from a queue;
- summary counts for dashboards.

## Requirements

- Normalize every record once at the ingestion boundary.
- Reject duplicate event ids.
- Use a list or tuple for ordered normalized events.
- Use dictionaries for id, source, and severity indexes.
- Use sets for tag membership.
- Use a deque-backed queue for FIFO alert processing.
- Drain events whose severity is greater than or equal to a configurable threshold.
- Requeue non-alert events while preserving their relative order.
- Return summary counts including total events, source count, tag count, alert count, and severity counts.
- Keep implementation code out of this prompt file.

## Example input

A useful smoke-test batch contains:

- `evt-2001`, source `sensor.edge-7`, severity 4, tags `edge`, `temperature`, `alert`;
- `evt-2002`, source `auth.gateway`, severity 5, tags `security`, `alert`;
- `evt-2003`, source `sensor.edge-7`, severity 1, tags `edge`, `heartbeat`;
- `evt-2004`, source `billing.worker`, severity 3, tags `billing`, `queue`.

## Expected behavior

- The id index retrieves each event by id in average O(1) time.
- The source index for `sensor.edge-7` returns `evt-2001` then `evt-2003`.
- The tag registry reports that `evt-2002` has `security` and `alert`.
- With minimum alert severity 4, the alert output contains `evt-2001` then `evt-2002`.
- The summary reports 4 total events, 3 sources, all unique tags, 2 alerts, and a count per severity.
- Mutating the original input after ingestion does not alter normalized event tags or top-level metadata.

## Hints

- Build small helpers first, then compose them.
- Keep error categories predictable so tests can assert specific exception types.
- Copy top-level metadata dictionaries and convert tags to tuples at the boundary.
- The full ingestion pass should be linear in the number of records plus their tags and metadata entries.
