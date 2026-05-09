"""Mutability, aliasing, and container costs.

Immutable primitives such as ``int``, ``str``, and ``tuple`` cannot be changed
in place. Mutable containers such as ``list`` and ``dict`` can be changed while
keeping the same identity. Aliasing happens when multiple variables reference the
same mutable object, so an in-place update through one name is visible through
all aliases.

Lists are dynamic arrays: appending is amortized O(1), indexing is O(1), and
inserting near the front is O(n). Dictionaries are hash tables: lookup, insert,
and update are O(1) average-case, with O(n) worst-case under heavy collisions or
resizing. Copying a sequence into a tuple is O(n) time and space.
"""


def append_tag_in_place(tags: list[str], tag: str) -> list[str]:
    """Append ``tag`` to ``tags`` and return the same list object.

    The append operation is amortized O(1); the function intentionally preserves
    aliasing to demonstrate shared mutable state.
    """

    tags.append(tag)
    return tags


def append_tag_copy(tags: tuple[str, ...] | list[str], tag: str) -> tuple[str, ...]:
    """Return a new tuple with ``tag`` appended without mutating ``tags``.

    Converting/copying the existing tags is O(n) time and space, but removes the
    caller-visible aliasing risk.
    """

    return tuple(tags) + (tag,)
