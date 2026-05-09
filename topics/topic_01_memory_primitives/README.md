# Topic 01: Memory & Primitives

Topic 01 builds the SentinelFlow foundation for reasoning about Python objects, references, primitive event records, mutability, aliasing, and memory cost. The slice uses only the Python standard library and keeps learning prompts separate from reference implementations.

## SentinelFlow Topic 01 Milestone

Define immutable and mutable event primitives; inspect identity, references, interning, and memory cost. By the end of this topic you should be able to explain when two event values are the same object, when they are merely equal, why mutable aliases can corrupt shared state, and how memory estimates change as event tags and metadata grow.

## Theory Overview

### Memory and primitives

Python variables hold references to objects. Each object has an identity, type, and value. Primitive-looking values such as strings and integers are still objects; containers store references to other objects. CPython manages most object lifetimes with reference counting and uses a cyclic garbage collector for reference cycles.

### Identity and equality

`is` checks whether two references point to the same object. This is O(1). `==` checks value equality and delegates to the object's equality implementation. Equality for fixed-size primitives is usually O(1), while list or tuple equality can be O(n) because Python may compare elements one by one.

### Mutability and aliasing

Mutable containers such as lists and dictionaries can be updated in place. If two variables reference the same mutable container, both observe changes through either alias. Immutable containers such as tuples cannot be changed in place, so updates require creating a new value. This is safer for event primitives but costs O(n) to copy n elements.

### Primitive object model

The topic starts with tuple-backed event primitives: `(event_id, source, severity, message)`. Tuple field access is O(1), construction for a fixed four-field tuple is O(1), and conversion to a fixed dictionary record is also O(1). Later modules normalize richer event records with tags and metadata.

### Interning

CPython may reuse small integers and identifier-like strings. `sys.intern` explicitly places strings into an intern table. Interning is an optimization detail: use `==` for correctness and never rely on `is` to decide whether two strings or integers have equal values.

### Copy and reference behavior

Assignment copies a reference in O(1). A shallow dictionary copy duplicates the top-level hash table entries in O(n), but nested mutable values remain shared. A deep copy recursively duplicates reachable values, using memoization to handle cycles; it is O(n) over the reachable object graph.

### Memory measurement

`sys.getsizeof` reports shallow size. Recursive estimates must walk supported containers and track visited object identities to avoid infinite recursion and double-counting cycles. The provided `deep_size` helper supports dictionaries, lists, tuples, sets, and frozensets in O(n) time and O(n) visited space.

## Complexity and Space Table

| Operation / Structure | Time Complexity | Space Complexity | Notes |
| --- | ---: | ---: | --- |
| Identity check with `is` | O(1) | O(1) | Compares object identity/reference. |
| Primitive equality | O(1) typical | O(1) | For ints/bools and fixed primitive values. |
| List/tuple equality | O(n) | O(1) extra | Stops early on mismatch. |
| List append | O(1) amortized | O(1) amortized | Dynamic array may resize. |
| Dict lookup/insert | O(1) average | O(1) extra | Hash-table backed; O(n) worst-case. |
| Tuple tag append by copy | O(t) | O(t) | Creates a new tuple of tags. |
| Metadata shallow copy | O(m) | O(m) | Top-level entries only. |
| Deep memory estimate | O(n) | O(n) | Traverses supported reachable containers with visited set. |
| PrimitiveEvent construction | O(t + m) | O(t + m) | Normalizes tags and metadata. |
| PrimitiveEvent field lookup | O(1) | O(1) | Slotted dataclass field access. |
| Tag index build | O(n * t) | O(n * t) | n events, t tags per event. |
| Tag index lookup | O(1) average + O(k) copy | O(k) | Returns tuple of k ids. |

## Folder Structure and File List

```text
topics/topic_01_memory_primitives/
├── README.md
├── concepts/
│   ├── __init__.py
│   ├── copy_reference.py
│   ├── identity_equality.py
│   ├── interning.py
│   ├── memory_measurement.py
│   ├── mutability_aliasing.py
│   └── primitive_object_model.py
├── dsa/
│   ├── __init__.py
│   ├── memory_inspector.py
│   ├── primitive_event.py
│   └── tag_index.py
├── errors/
│   ├── __init__.py
│   ├── aliasing_shared_state.py
│   ├── event_validation.py
│   └── immutable_type_errors.py
├── lab/
│   ├── advanced_challenge.md
│   ├── entry_challenge.md
│   └── mid_challenge.md
├── solutions/
│   ├── __init__.py
│   ├── advanced_solution.py
│   ├── entry_solution.py
│   └── mid_solution.py
└── tests/
    ├── __init__.py
    └── test_suite.py
```

## Learning Outcomes

After completing this topic, you can:

- Distinguish object identity from value equality.
- Explain why equality cost depends on the underlying data structure.
- Demonstrate list aliasing and avoid it with immutable tuple copies.
- Validate primitive event records with clear `KeyError`, `ValueError`, and `TypeError` boundaries.
- Normalize event tags and metadata without leaking caller-owned mutable state.
- Use a frozen, slotted dataclass to model immutable SentinelFlow events.
- Estimate shallow vs recursive memory cost and handle cycles safely.
- Build and query a hash-table-backed tag index.
- Keep lab prompts free of solution implementations.

## Running Tests

Run the focused Topic 01 suite:

```bash
python -m unittest discover -s topics/topic_01_memory_primitives/tests -p 'test_suite.py'
```

Run all topic test suites from the topics root:

```bash
python -m unittest discover -s topics -p 'test_suite.py'
```
