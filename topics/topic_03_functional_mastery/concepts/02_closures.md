# Closures

A closure is a function that remembers values from the lexical scope where it was created. SentinelFlow uses closures for configured stages such as `require_fields("id", "level")`, `require_level(allowed)`, and `add_route("alerts")`.

SentinelFlow example: `require_level({"error", "critical"})` builds a set once, then the returned validator checks each event's level against that captured set. The pipeline receives a simple unary stage even though the stage carries configuration.

Underlying structures include closure cells for captured values, sets for allowed-level membership, event dictionaries for payloads, and stack frames for calls.

Complexity: creating a closure is O(c) for captured setup. Converting `a` allowed levels to a set is O(a) time and O(a) space. Each membership check is O(1) average. Captured configuration avoids rebuilding the same data structure for every event.
