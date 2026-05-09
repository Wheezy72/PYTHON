# Entry Challenge: Identity, Equality, and Event Primitives

Build a small set of immutable SentinelFlow event primitives and inspect how Python stores and compares them.

## Requirements

- Create a helper that builds an immutable event tuple with event id, source, severity, and message.
- Convert that tuple into a dictionary record without mutating the tuple.
- Build two separate event tuple values with equal contents.
- Inspect whether the two values have the same identity and the same value.
- Report object ids and type names so you can explain references vs values.

## Hints

- Use `is` for identity and `==` for equality.
- Tuple field access by index is O(1).
- Tuple equality may compare fields, so it depends on the number and size of compared fields.

## Tiny data example

A realistic event might use `"evt-1001"`, `"sensor.edge-7"`, severity `3`, and a short message such as `"temperature threshold crossed"`.

## Expected behavior

- Two equal tuples should compare equal by value.
- Two independently created tuples should not be required to share identity.
- The record form should contain the same four primitive fields.
