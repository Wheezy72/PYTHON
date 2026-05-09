# Advanced Challenge: SentinelFlow Functional Ingestion

Build a complete functional ingestion pipeline for SentinelFlow events. The pipeline should combine pure transforms, decorator-based validation, closure counters, configured enrichment, and defensive error handling.

## Requirements

- Accept realistic event records with identifiers, sources, severities, messages, tags, and metadata.
- Validate required fields and severity range before accepting an event.
- Normalize messages and tag storage without mutating input records.
- Add an ingestion tag exactly once.
- Enrich events with a configured region derived from metadata or a safe fallback.
- Count accepted events and accepted events by source using closure-backed counters.
- Collect rejected records with their input index and a useful error message.
- Produce a summary containing accepted events, source counts, accepted count, and rejected details.

## Error-First Expectations

Validate every pipeline stage before it runs. Wrap stage failures with context that identifies the failed stage. Keep original exceptions available for debugging when wrapping errors.

## Complexity Targets

Process n events in a single pass. Source counts should use dictionary-backed O(1) average updates. Each accepted event may copy O(f + t + m) data for fields, tags, and metadata.
