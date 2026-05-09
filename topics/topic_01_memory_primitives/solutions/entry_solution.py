"""Reference solution for the Topic 01 entry challenge."""

from ..concepts.identity_equality import identity_report
from ..concepts.primitive_object_model import build_event_tuple, event_tuple_to_record


def make_event_identity_snapshot(event_id, source, severity, message) -> dict[str, object]:
    """Build equal tuple events and report identity/equality plus record form."""

    left_event = build_event_tuple(event_id, source, severity, message)
    right_event = build_event_tuple(event_id, source, severity, message)
    return {
        "left_event": left_event,
        "right_event": right_event,
        "identity_report": identity_report(left_event, right_event),
        "record": event_tuple_to_record(left_event),
    }
