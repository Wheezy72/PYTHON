# Lambdas

A lambda is a small anonymous function expression. SentinelFlow can use lambdas for short predicates after events are validated and normalized, such as selecting only `error` or `critical` events.

SentinelFlow example: a batch can call `filter_events(events, lambda event: event["level"] in {"error", "critical"})` after normalization. The lambda is still a function object and can capture surrounding values through closure rules.

Underlying structures include function objects, closure cells for captured values, iterable traversal over event batches, and list accumulation for retained events.

Complexity: creating a lambda is O(1). Filtering `n` events with predicate cost `p` is O(n * p). The output list stores `r` retained event references, so space is O(r). Complex validation should use named functions because lambdas have no docstring and poor trace names.
