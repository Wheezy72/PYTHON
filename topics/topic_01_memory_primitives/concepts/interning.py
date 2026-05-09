"""CPython interning observations.

CPython reuses some immutable objects, notably small integers and some
identifier-like strings. ``sys.intern`` explicitly interns strings in a process
wide table so equal strings can share identity. Interning can make equality
checks faster after a hash lookup, but correctness must never depend on whether
``a is b`` for equal strings or integers; use ``==`` for value equality.
"""

import sys


def interning_observation(value: str) -> dict[str, object]:
    """Return observable facts about explicit string interning.

    String equality is O(n) in the string length in the worst case. Interning the
    string inserts or finds it in a hash-table-like intern table.
    """

    interned = sys.intern(value)
    return {
        "value": value,
        "interned": interned,
        "equal": value == interned,
        "same_identity_after_intern": value is interned,
        "value_id": id(value),
        "interned_id": id(interned),
    }
