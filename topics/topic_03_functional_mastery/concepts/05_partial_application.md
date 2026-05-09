# Partial Application

Partial application pre-fills part of a function's input so the result is a more specific callable. SentinelFlow uses closure-style partial application for helpers such as `add_route("payments")` and `enrich_with_source("edge")`.

SentinelFlow example: instead of passing both route and event at every call, configure the route once and return a unary transformer. Unary stages compose cleanly with `pipe` and `compose`.

Underlying structures include closure cells or `functools.partial` objects, event dictionaries, and stage lists containing one-argument callables.

Complexity: creating a specialized callable is O(1) for simple captured values. Copying a `k`-key event before adding metadata is O(k) time and O(k) space. Running `s` partially applied stages is O(s) plus each stage's copying, lookup, or validation cost.
