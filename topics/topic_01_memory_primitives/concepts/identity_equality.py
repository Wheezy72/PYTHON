"""Identity, equality, and object references.

Python variables hold references to objects. The ``is`` operator checks whether
both references point at the exact same object, so identity checks are O(1):
Python compares object addresses/handles rather than walking object contents.

The ``==`` operator asks whether two objects have the same value. Its complexity
is type-dependent. Integer and boolean equality are O(1), while container
comparison can inspect many elements. For example, list equality is O(n) in the
number of compared elements, stopping early when a mismatch is found.
"""


def identity_report(left: object, right: object) -> dict[str, object]:
    """Return identity and equality facts for two references.

    ``id`` and ``type`` lookups are O(1). The equality result may be more
    expensive depending on the underlying value type; list equality is O(n).
    """

    return {
        "same_identity": left is right,
        "same_value": left == right,
        "left_id": id(left),
        "right_id": id(right),
        "left_type": type(left).__name__,
        "right_type": type(right).__name__,
    }
