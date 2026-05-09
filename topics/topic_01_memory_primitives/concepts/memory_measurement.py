"""Memory measurement helpers.

``sys.getsizeof`` reports the shallow size of a Python object: the object's own
storage, not necessarily the objects it references. Recursive estimates are
approximate because interpreter internals, shared references, allocator overhead,
and cached/interned objects complicate exact accounting.

``deep_size`` walks supported containers recursively with a visited-id set to
avoid double-counting shared objects and to terminate on cycles. Traversal is
O(n) time over the reachable supported object graph and O(n) space for visited
identities.
"""

from __future__ import annotations

import sys
from collections.abc import Mapping

_CONTAINER_TYPES = (dict, list, tuple, set, frozenset)


def shallow_size(obj: object) -> int:
    """Return ``sys.getsizeof(obj)`` as a shallow byte estimate."""

    return sys.getsizeof(obj)


def deep_size(obj: object) -> int:
    """Recursively estimate size for dict/list/tuple/set/frozenset containers."""

    visited: set[int] = set()

    def walk(value: object) -> int:
        object_id = id(value)
        if object_id in visited:
            return 0
        visited.add(object_id)

        total = sys.getsizeof(value)
        if isinstance(value, Mapping):
            for key, item in value.items():
                total += walk(key)
                total += walk(item)
        elif isinstance(value, (list, tuple, set, frozenset)):
            for item in value:
                total += walk(item)
        return total

    return walk(obj)
