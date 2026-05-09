# Mid Challenge: Decorator Validation and Configured Predicates

Create a SentinelFlow alert helper that validates records before transformation and filters transformed results with configured predicates. This challenge focuses on decorators, predicate factories, and readable functional contracts.

## Requirements

- Validate that each event contains the required SentinelFlow fields.
- Validate that severity is an integer in the accepted inclusive range.
- Preserve wrapped function metadata so diagnostics show the original transform name.
- Enrich valid records by normalizing the message and adding a validation tag.
- Build a configured predicate for a minimum severity threshold.
- Keep only enriched records that satisfy the threshold.

## Defensive Expectations

Missing fields should raise a helpful key error. Invalid severity should raise a helpful value error. Predicate logic should remain small and named when it stops being obvious.

## Complexity Targets

Validation checks should be linear in the number of required fields. Filtering should scan records once and preserve order. Tag membership costs depend on whether tags are list, tuple, or set backed.
