# Topic 02: Linear DSA & Error Architecture

Topic 02 builds SentinelFlow's first in-memory indexing layer. It uses Python lists, dictionaries, sets, and `collections.deque` to store event streams, accelerate lookups, model tag membership, and process FIFO alert queues. The slice uses only the Python standard library and keeps lab prompts separate from importable reference solutions.

No third-party dependencies are required.

## SentinelFlow Topic 02 Milestone

Build in-memory event indexes with lists, dicts, sets, and queues; add error taxonomy for invalid events.

## Learning Outcomes

After completing this topic, you can:

- Explain how Python lists act as dynamic arrays and why copying or slicing costs O(n).
- Build dictionary-backed indexes for event id, source, and severity lookup.
- Use sets and frozensets for fast tag membership and immutable query results.
- Use `collections.deque` for FIFO queues without O(n) front-removal shifts.
- Compare time and space tradeoffs across lists, dicts, sets, and deques.
- Validate SentinelFlow records with clear `KeyError`, `TypeError`, `ValueError`, and `IndexError` boundaries.
- Normalize event records without leaking mutable caller-owned tags or top-level metadata.
- Compose indexes, tag registries, queues, defensive lookup helpers, and summaries into a small ingestion pipeline.

## Theory Overview

### Lists: dynamic arrays for ordered streams

Python lists store references in a contiguous dynamic array. Indexing by position is O(1), scanning is O(n), and append is O(1) amortized because Python over-allocates capacity and occasionally resizes. Topic 02 uses lists for ordered event streams and returns copied lists where aliasing safety is more important than avoiding O(n) copy cost.

Key module: `concepts/list_internals.py`.

### Dictionaries: hash tables for event indexes

Dictionaries map hashable keys to values with average O(1) lookup and insertion. They use extra table space to avoid repeated linear scans. An event id index turns “find event `evt-2002`” from O(n) list search into average O(1) dictionary lookup. Source and severity indexes use dictionaries whose values are ordered lists of normalized event records, combining fast group access with insertion-order preservation inside each group.

Key modules: `concepts/dict_hash_table.py` and `dsa/event_index.py`.

### Sets: hash-backed membership

Sets store unique hashable values and provide average O(1) membership tests. Topic 02 uses sets to represent tag membership and registry internals. Frozensets are immutable sets, useful for returning safe views from `TagRegistry` and for normalized required-tag filters.

Key modules: `concepts/set_membership.py`, `errors/hashability_type_error.py`, and `dsa/tag_registry.py`.

### Deques: FIFO queues

`collections.deque` is optimized for appends and pops at both ends. A list can append at the right in O(1) amortized time, but removing from the front requires shifting remaining elements and costs O(n). `SeverityQueue` uses a deque to enqueue normalized events, peek/dequeue FIFO events, and drain high-severity alerts while requeueing lower-severity events in relative order.

Key modules: `concepts/queue_deque.py` and `dsa/severity_queue.py`.

### Hashing, resizing, membership, and indexing

Dicts and sets hash keys to choose table positions. Average O(1) behavior depends on hash distribution and table load. Python resizes hash tables as they fill, which occasionally costs O(n), but keeps normal operations fast on average. The space tradeoff is deliberate: indexes and registries duplicate references and grouping containers so repeated lookups avoid repeated scans.

### Aliasing safety at ingestion boundaries

Indexes should contain normalized snapshots, not direct caller-owned mutable structures. Topic 02 converts tags to tuples and shallow-copies metadata dictionaries. This prevents common bugs where code mutates the original input after ingestion and accidentally changes indexed events.

Key module: `errors/value_error_validation.py`.

## Big O and Space Complexity Table

| Structure / Operation | Time Complexity | Space Complexity | Notes |
| --- | ---: | ---: | --- |
| List index by position | O(1) | O(1) | Direct dynamic-array offset. |
| List append in place | O(1) amortized | O(1) amortized | Occasional O(n) resize. |
| Copy-and-append event stream | O(n) | O(n) | Safer API boundary used by `append_event`. |
| List slice/window copy | O(k) | O(k) | Copies k references for recent events. |
| List linear scan | O(n) | O(1) | Used when no index exists. |
| Dict lookup/insert | O(1) average | O(1) per entry | O(n) worst case under collisions or resize. |
| Build id index | O(n) | O(n) | One hash-table entry per event. |
| Build source/severity indexes | O(n) | O(n) | Grouped lists preserve insertion order. |
| Set membership/insert | O(1) average | O(1) per tag/id | Requires hashable values. |
| Build tag registry | O(n * t) | O(n * t) | t is average tags per event. |
| Frozenset result copy | O(k) | O(k) | Protects registry internals. |
| Deque enqueue/dequeue/peek | O(1) | O(1) per event | No front-shift cost. |
| Drain queue once | O(n) | O(a + r) | a alerts returned, r retained events requeued. |
| Normalize event record | O(t + m) | O(t + m) | Copies tags and top-level metadata. |
| Batch required lookup | O(k) average | O(k) | Reports all missing keys together. |

## Error Architecture and Defensive Patterns

Topic 02 separates error categories by cause:

- `KeyError`: a required field or lookup key is missing.
- `TypeError`: a value has the wrong container or field type, such as metadata that is not a dictionary or a tag that is not a string.
- `ValueError`: a value has the right general shape but invalid content, such as blank strings, duplicate event ids, or severity outside 1..5.
- `IndexError`: a positional access is outside list bounds.
- `unknown`: an uncategorized exception that should not be silently swallowed.

Use natural exceptions when a field, key, or position is required. Use defensive helpers such as `dict.get`, safe list access, and batch missing-key collection when absence is expected and should be reported cleanly.

Key modules:

- `concepts/error_architecture_basics.py` defines `EventValidationError`, `EventShapeError`, and exception classification.
- `errors/index_error_patterns.py` compares natural list `IndexError` with safe positional lookup.
- `errors/key_error_patterns.py` compares required dictionary access with defensive `.get`.
- `errors/hashability_type_error.py` validates non-blank string tags for set membership.
- `errors/value_error_validation.py` validates and normalizes SentinelFlow event records.
- `errors/defensive_lookup.py` centralizes optional, required, and batch lookup patterns.
- `dsa/safe_lookup.py` wraps defensive lookup helpers for reusable index queries.

## Structure and Module Guide

```text
topic_02_linear_dsa_error_architecture/
├── README.md
├── __init__.py
├── concepts/
│   ├── __init__.py
│   ├── list_internals.py
│   ├── dict_hash_table.py
│   ├── set_membership.py
│   ├── queue_deque.py
│   ├── big_o_tradeoffs.py
│   └── error_architecture_basics.py
├── errors/
│   ├── __init__.py
│   ├── index_error_patterns.py
│   ├── key_error_patterns.py
│   ├── hashability_type_error.py
│   ├── value_error_validation.py
│   └── defensive_lookup.py
├── dsa/
│   ├── __init__.py
│   ├── event_index.py
│   ├── severity_queue.py
│   ├── tag_registry.py
│   └── safe_lookup.py
├── lab/
│   ├── entry_challenge.md
│   ├── mid_challenge.md
│   └── advanced_challenge.md
├── solutions/
│   ├── __init__.py
│   ├── entry_solution.py
│   ├── mid_solution.py
│   └── advanced_solution.py
└── tests/
    ├── __init__.py
    └── test_suite.py
```

### Concepts

- `concepts/list_internals.py`: event streams as dynamic arrays; copy-and-append, recent slicing, and linear id scan.
- `concepts/dict_hash_table.py`: event id and source indexes as hash tables; average O(1) id lookup.
- `concepts/set_membership.py`: tags as hash-backed sets; unique tags, all-required-tags filtering, and tag normalization.
- `concepts/queue_deque.py`: FIFO queue helpers built on `collections.deque`.
- `concepts/big_o_tradeoffs.py`: compact complexity table and access-pattern recommendations.
- `concepts/error_architecture_basics.py`: error taxonomy and classification helpers.

### Errors

- `errors/index_error_patterns.py`: natural `IndexError` access and safe index fallback.
- `errors/key_error_patterns.py`: required field access and optional field fallback.
- `errors/hashability_type_error.py`: non-string and blank-tag validation for set membership.
- `errors/value_error_validation.py`: SentinelFlow record validation and alias-safe normalization.
- `errors/defensive_lookup.py`: safe lookup, required lookup, and missing-key collection.

### DSA

- `dsa/event_index.py`: `EventIndex` with `by_id`, `by_source`, and `by_severity` dictionaries.
- `dsa/severity_queue.py`: `SeverityQueue` backed by `collections.deque` with high-severity draining.
- `dsa/tag_registry.py`: `TagRegistry` backed by dictionaries of sets.
- `dsa/safe_lookup.py`: small reusable wrappers for optional/default/required batch lookup.

### Labs and Solutions

- `lab/entry_challenge.md`: prompt for building an event id/source index.
- `lab/mid_challenge.md`: prompt for tag registry plus defensive validation.
- `lab/advanced_challenge.md`: prompt for full in-memory ingestion with indexes, severity queue, and errors.
- `solutions/entry_solution.py`: `build_event_indexes(records)` using `EventIndex`.
- `solutions/mid_solution.py`: `build_tag_registry(records)` and `filter_events_by_tags(records, required_tags)`.
- `solutions/advanced_solution.py`: `ingest_sentinelflow_events(records, min_alert_severity=4)` returning normalized events, index, registry, alerts, and summary counts.

## Lab Overview

The lab path moves from individual structures to a composed ingestion milestone:

1. Entry challenge: build an event id/source index and reason about list scans versus dictionary lookup.
2. Mid challenge: add a hash-backed tag registry and defensive validation boundaries.
3. Advanced challenge: compose normalized events, `EventIndex`, `TagRegistry`, `SeverityQueue`, and summary counts into a complete in-memory SentinelFlow ingestion pipeline.

Lab markdown files are prompts only. They provide requirements, hints, example inputs, and expected behavior without function bodies, class bodies, or importable solution snippets.

## Running Tests

Run the focused Topic 02 suite from the repository root:

```bash
python -m unittest discover -s topics/topic_02_linear_dsa_error_architecture/tests -p 'test_suite.py'
```

When neighboring topics are stable, run the full topic discovery suite:

```bash
python -m unittest discover -s topics -p 'test_suite.py'
```

The Topic 02 tests validate concept helpers, error behavior, DSA modules, solution modules, prompt-only lab files, and a realistic SentinelFlow integration smoke test.
