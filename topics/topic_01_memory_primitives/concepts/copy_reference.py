"""Assignment, shallow copy, and deep copy.

Assignment copies a reference in O(1); both names still point to the same object.
A shallow ``dict.copy`` is O(n) for top-level keys but nested mutable metadata is
still shared. ``copy.deepcopy`` recursively copies nested containers, so it is
O(n) over the reachable object graph and uses memoization to preserve cycles.
"""

from copy import deepcopy


def reference_copy_metadata(metadata: dict[str, object]) -> dict[str, object]:
    """Return the original metadata reference in O(1)."""

    return metadata


def shallow_copy_metadata(metadata: dict[str, object]) -> dict[str, object]:
    """Return a top-level copy; nested mutable values remain aliased."""

    return metadata.copy()


def deep_copy_metadata(metadata: dict[str, object]) -> dict[str, object]:
    """Return a recursive copy of metadata, protecting nested mutable values."""

    return deepcopy(metadata)
