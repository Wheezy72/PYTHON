# Purity and Side Effects

A pure function returns the same output for the same input and does not mutate external state. SentinelFlow transformers should return new event dictionaries instead of editing raw ingress events in place.

SentinelFlow benefits: raw events can be logged, retried, routed to multiple destinations, or compared in tests without one stage changing another stage's input. Side effects such as timing or audit counts are still useful, but they should be explicit and isolated on decorator wrappers.

Underlying structures include shallow dictionary copies for top-level event fields, lists returned by map/filter helpers, and wrapper attributes for operational metadata.

Complexity: shallow-copying a `k`-key event costs O(k) time and O(k) space. Pure predicates filter `n` events in O(n * p) time with O(r) output space. Audit and timing attributes add O(1) wrapper storage.
