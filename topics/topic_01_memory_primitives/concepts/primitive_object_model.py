"""Python's primitive object model.

Every Python value is an object with identity, type, and value. Variables store
references to objects rather than raw inline values. CPython manages object
lifetime primarily through reference counting plus a cyclic garbage collector for
reference cycles.

A small immutable event tuple is useful for foundational learning: field access
by tuple index is O(1), tuple construction is O(k) for k fields, and immutable
storage prevents accidental in-place mutation of event primitives.
"""

EventTuple = tuple[str, str, int, str]


def build_event_tuple(
    event_id: str, source: str, severity: int, message: str
) -> EventTuple:
    """Build an immutable event tuple in O(1) for the fixed four fields."""

    return (event_id, source, severity, message)


def event_tuple_to_record(event: EventTuple) -> dict[str, object]:
    """Convert a fixed event tuple to a dict record.

    Tuple field access is O(1) per field; creating the four-field dictionary is
    O(1) for this fixed-size shape.
    """

    event_id, source, severity, message = event
    return {
        "event_id": event_id,
        "source": source,
        "severity": severity,
        "message": message,
    }
