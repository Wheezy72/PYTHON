# Topic 04: Advanced OOP

Topic 04 turns SentinelFlow into an extensible object model. It covers MRO, cooperative `super`, mixins, ABCs, runtime-checkable protocols, dataclasses, composition, and polymorphic event processors.

## SentinelFlow milestone

Introduce event processors, storage interfaces, mixins, ABCs, and composition-based services.

## Complexity overview

| Operation | Time | Space | Structure |
| --- | ---: | ---: | --- |
| Processor dispatch | O(p * c) | O(1) extra | p processors, c processor cost |
| Registry lookup | O(1) average | O(n) | Dict hash table |
| In-memory store add | O(1) amortized | O(n) | List dynamic array |
| Source grouping | O(n) | O(k) | Dict of lists |
| MRO lookup | O(m) worst | O(m) cached metadata | Class linearization |

## Learning outcomes

- Explain C3 MRO and why cooperative `super()` matters.
- Use mixins for small reusable behavior.
- Use ABCs and Protocols to define object contracts.
- Prefer composition when behavior varies independently.
- Build a polymorphic SentinelFlow processor pipeline.

## Tests

```bash
python -m unittest discover -s topics/topic_04_advanced_oop/tests -p 'test_suite.py'
```
