# Higher-Order Functions

A higher-order function accepts functions, returns functions, or both. SentinelFlow relies on higher-order functions for validator factories, decorators, map/filter helpers, and composition utilities.

SentinelFlow examples include `require_fields(*fields)` returning a validator, `filter_events(events, predicate)` accepting a predicate, and `preserve_metadata_decorator(label)` returning a decorator.

Underlying structures include iterables for incoming batches, lists for mapped or filtered results, dictionaries for event payloads and counts, and function objects passed through the pipeline.

Complexity: building a higher-order stage is usually O(1), except setup such as converting allowed levels to a set. Mapping `n` events costs O(n * t), where `t` is transformer cost, and returns O(n) output. Filtering costs O(n * p) and stores O(r) retained events.
