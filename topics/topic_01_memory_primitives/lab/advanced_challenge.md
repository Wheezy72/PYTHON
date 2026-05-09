# Advanced Challenge: Memory-Aware PrimitiveEvent Tooling and Tag Index

Build runtime tooling around immutable SentinelFlow event objects.

## Requirements

- Represent a normalized event as an immutable, slotted data object.
- Provide conversion from and to primitive dictionary records.
- Add tags by returning a new event rather than mutating an existing one.
- Estimate shallow and recursive memory use for event records, tags, metadata, and messages.
- Build a tag index that maps each tag to the event ids that contain it.
- Summarize memory use across a sequence of events.

## Hints

- A hash-table-backed dictionary gives average O(1) lookup by tag.
- Building a tag index is O(n * t), where n is event count and t is tags per event.
- Recursive memory estimation needs a visited set to avoid infinite loops on cycles.
- Frozen data objects preserve caller-facing immutability, but construction can still normalize defensively.

## Tiny data example

Use a few events from different sources, with overlapping tags such as `"edge"`, `"security"`, and `"heartbeat"`, to prove that the index groups ids correctly.

## Expected behavior

- Event instances cannot be modified through normal attribute assignment.
- The tag index returns all matching event ids and an empty result for missing tags.
- Memory summaries include count, total deep size, average deep size, and max deep size.
