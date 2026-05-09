# Mid Challenge: Defensive Event Validation and Aliasing Safety

Validate SentinelFlow event records before they move deeper into the system, then normalize mutable inputs into safer forms.

## Requirements

- Require these fields: event id, source, severity, message, tags, and metadata.
- Raise a missing-field error for incomplete records.
- Raise a value error for invalid severity, empty string fields, non-string tags, or non-dictionary metadata.
- Normalize tags into an immutable tuple.
- Shallow-copy metadata so callers cannot mutate your top-level record metadata by alias.
- Add a tag without mutating the original record or reusing the original tag container.

## Hints

- Validation is a defensive boundary: fail early and clearly.
- Lists are dynamic arrays; appending is amortized O(1), but aliases see the mutation.
- Copying tags to a tuple is O(t), where t is the number of tags.
- Shallow metadata copying is O(m) for m top-level entries.

## Tiny data example

A record can include tags such as `"edge"` and `"temperature"`, plus metadata like a region or device id. Keep examples small; your solution should work for larger records too.

## Expected behavior

- Valid records return normalized copies.
- Invalid records raise the appropriate exception.
- Adding a tag returns a new record and leaves the input unchanged.
