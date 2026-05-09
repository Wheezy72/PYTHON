# Entry Challenge: Event Log and Safe Index Access

Build the first SentinelFlow event-log layer using a Python list as a dynamic array.

## Requirements

- Accept a sequence of event dictionaries.
- Validate records before they enter the event log.
- Store events in arrival order.
- Read one event by index with a clear error when the index is invalid.
- Return immutable snapshots of event ids and replay windows.

## Complexity questions

- Why is appending to a Python list amortized O(1)?
- Why is reading by index O(1)?
- Why does copying a replay window cost O(k)?
