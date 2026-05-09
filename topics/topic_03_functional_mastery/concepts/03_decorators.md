# Decorators

A decorator is a higher-order function that receives a function and returns a replacement function. SentinelFlow uses decorators for cross-cutting concerns such as audit labels, call counts, and stage timing.

SentinelFlow example: `timed_stage` wraps a transformer and records `last_duration_seconds`. An audit decorator can attach `audit_metadata` while leaving validation and transformation logic unchanged.

Good decorators use `functools.wraps` so `__name__`, `__doc__`, and `__wrapped__` still point back to the original stage. This matters for logs, tests, introspection, and debugging production ingestion flows.

Underlying structures include wrapper function objects, one extra wrapper stack frame per decorator layer, and small dictionaries or attributes attached to wrappers.

Complexity: decoration is O(1) for typical metadata copying. Each decorator call adds O(1) overhead plus the wrapped work. Stacking `d` decorators adds O(d) wrapper frames and O(d) constant overhead.
