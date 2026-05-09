"""Immutable-type errors and safe alternatives.

Tuples are immutable. Attempting item assignment raises ``TypeError`` naturally,
which is more honest than hiding an invalid mutation behind broad exception
handling. The safe pattern is to build a new tuple, an O(n) operation over the
existing tuple length.
"""


def attempt_tuple_tag_mutation(tags: tuple[str, ...], tag: str) -> None:
    """Deliberately attempt to mutate a tuple and let ``TypeError`` surface."""

    tags[0] = tag  # type: ignore[index]


def safe_extend_tuple_tags(tags: tuple[str, ...], tag: str) -> tuple[str, ...]:
    """Return a new tuple containing existing tags plus ``tag``."""

    return tags + (tag,)
