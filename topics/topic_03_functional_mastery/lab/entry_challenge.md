# Entry Challenge: Pure Transform Pipeline

Build a small SentinelFlow transform pipeline that accepts event records and creates new records. Practice pure functions and composition without mutating caller-owned data.

## Requirements

- Accept an iterable of dictionary-like event records.
- Normalize each message by trimming whitespace, collapsing repeated spaces, and using lowercase text.
- Cap severities above the allowed maximum to the maximum value.
- Add a processed tag exactly once.
- Preserve existing tags and metadata without sharing mutable containers with the caller.
- Keep records in the original order.

## Complexity Targets

Use a single pass over n records. Copy only the top-level record, tags, and metadata that need protection. Explain why dictionary copy is O(f) for f fields and tag copy is O(t) for t tags.

## Hints

Think in small unary transforms. Compose or pipe the transforms left-to-right. Test that changing the original input after the pipeline runs does not change the output.
