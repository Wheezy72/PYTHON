# Entry Challenge: Event Id and Source Indexes

Build the first SentinelFlow in-memory index layer for event lookup.

## Requirements

- Accept a sequence of event dictionaries.
- Validate and normalize records before indexing them.
- Preserve arrival order in the normalized `events` snapshot.
- Build an id index that maps each `event_id` to its normalized record.
- Build a source index that maps each source to its events in arrival order.
- Build a severity index that maps each severity level to its events in arrival order.
- Reject duplicate event ids with a clear error.
- Return immutable snapshots from grouped indexes so callers cannot mutate internal lists.

## Complexity questions

- Why does an id dictionary make event lookup average O(1)?
- Why does building all indexes cost O(n) plus tag and metadata normalization cost?
- What extra O(n) space do the indexes use compared with scanning a list?
