# Mid Challenge: Source and Severity Indexes

Build secondary indexes for SentinelFlow event records using dictionaries and sets.

## Requirements

- Validate incoming records.
- Build a source index from source name to event ids.
- Build a severity index from severity level to event ids.
- Preserve event arrival order inside each index bucket.
- Detect duplicate event ids using set membership.
- Return empty results for missing lookups.

## Complexity questions

- What is the average-case cost of dictionary insertion?
- When is a scan better than maintaining an index?
