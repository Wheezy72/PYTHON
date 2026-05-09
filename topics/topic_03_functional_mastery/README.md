# Topic 03: Functional Mastery

Topic 03 builds the SentinelFlow foundation for functional Python: closures, decorators, predicate factories, higher-order functions, partial application, pure transforms, composition, and defensive functional error handling. The slice uses only the Python standard library and keeps lab prompts separate from reference implementations.

## SentinelFlow Topic 03 Milestone

Build decorator-based validation and transformation pipelines for SentinelFlow events. By the end of this topic you should be able to validate event records with decorators, compose pure transformations, configure predicates and enrichers, count stream state with closures, and wrap pipeline failures with useful error context.

## Theory Overview

### Closures

A closure keeps variables from an outer scope alive after that outer function returns. Topic 03 uses closures for event counters, source filters, severity trackers, key counters, and deterministic rate limiters. Closures are appropriate when the state is small, local, and easier to reason about than a global variable or class.

### Decorators

Decorators wrap callables to add cross-cutting behavior such as validation or stage annotation. Validation decorators enforce required fields and severity ranges before transforms run. `functools.wraps` is required for production-quality decorators because it preserves metadata such as function names and docstrings.

### Lambdas and predicate factories

Lambdas are useful for tiny predicates passed near their use site. When logic becomes dense, a named predicate factory such as `severity_at_least(4)` or `has_tag("edge")` is clearer and easier to test. Topic 03 includes deterministic readability checks that flag overly complex anonymous predicate snippets.

### Higher-order functions

Higher-order helpers accept callables to map, filter, reduce, and group events. The key contract is explicit: mapping transforms return records, predicates return booleans, and key functions return hashable grouping keys.

### Partial application

Partial application binds configuration early and produces a simpler callable for the pipeline. SentinelFlow uses this for configured region enrichers, constant-field transforms, and message prefixing.

### Pure functions and composition

Pure transforms return new records rather than mutating inputs. This prevents aliasing bugs when tags or metadata are shared by the caller. Composition helpers such as `compose`, `pipe`, and `Pipeline` connect small unary transforms into readable ingestion flows.

### Functional error patterns

Functional pipelines should validate callable contracts before invoking stages and should add stage context when failures occur. Topic 03 demonstrates helpful `TypeError` boundaries and a `FunctionalPipelineError` wrapper that preserves original exceptions as causes.

## Complexity and Space Table

| Operation / Structure | Time Complexity | Space Complexity | Notes |
| --- | ---: | ---: | --- |
| Closure scalar counter increment | O(1) | O(1) | Integer state enclosed by a function. |
| Dict-backed count update | O(1) average | O(k) | Hash table stores k distinct keys; worst-case collisions can degrade. |
| Required-field validation | O(r) | O(m) | Checks r required names and stores m missing names. |
| Severity range validation | O(1) | O(1) | Single field check. |
| List/tuple tag membership | O(t) | O(1) | Scans t tags. |
| Set tag membership | O(1) average | O(1) | Hash-table backed. |
| Filter n records | O(n * p) | O(k) | p is predicate cost; k accepted records are stored. |
| Partition n records | O(n * p) | O(n) | Stores accepted and rejected lists. |
| Map n records | O(n * c) | O(n) | c is transform cost. |
| Reduce counts by key | O(n) average | O(k) | Dictionary-backed grouping. |
| Top-level record copy | O(f) | O(f) | f dictionary fields copied. |
| Tag copy or append | O(t) | O(t) | Tuple/list conversion and append-by-copy. |
| Metadata shallow copy | O(m) | O(m) | m metadata keys copied. |
| Compose or Pipeline construction | O(k) | O(k) | Stores k validated callable stages in a tuple. |
| Pipeline execution | O(k + stage costs) | O(1) extra | Runs k stages, keeping current value. |

## Folder Structure and File Guide

```text
topics/topic_03_functional_mastery/
├── README.md
├── concepts/
│   ├── closures.py
│   ├── decorators.py
│   ├── higher_order.py
│   ├── lambda_predicates.py
│   ├── partial_application.py
│   └── pure_composition.py
├── dsa/
│   ├── closure_counters.py
│   ├── decorator_validators.py
│   ├── pipeline.py
│   └── predicate_filters.py
├── errors/
│   ├── callable_contracts.py
│   ├── decorator_metadata.py
│   ├── functional_defensive_patterns.py
│   ├── lambda_readability.py
│   └── late_binding_closures.py
├── lab/
│   ├── advanced_challenge.md
│   ├── entry_challenge.md
│   └── mid_challenge.md
├── solutions/
│   ├── advanced_solution.py
│   ├── entry_solution.py
│   └── mid_solution.py
└── tests/
    └── test_suite.py
```

Additional markdown concept and error guides may be present as reading material; executable implementations live in the Python modules listed above.

## Learning Outcomes

After completing this topic, you can:

- Use closures for small, explicit state such as counters and configured filters.
- Explain how dictionary, tuple, list, and set backing structures affect functional helper complexity.
- Write decorators that validate event records and preserve callable metadata.
- Replace dense lambdas with named predicate factories.
- Build higher-order map, filter, reduce, and predicate-composition helpers.
- Use partial application to configure transforms without global variables.
- Compose pure transforms that avoid mutating input records or leaking mutable aliases.
- Validate callable contracts and wrap pipeline errors with stage context.
- Build a complete SentinelFlow ingestion pipeline that separates accepted and rejected records.
- Keep lab prompts free of solution implementations.

## Running Tests

Run the focused Topic 03 suite from the repository root:

```bash
python -m unittest discover -s topics/topic_03_functional_mastery/tests -p 'test_suite.py'
```

Run all topic suites from the repository root:

```bash
python -m unittest discover -s topics -p 'test_suite.py'
```
