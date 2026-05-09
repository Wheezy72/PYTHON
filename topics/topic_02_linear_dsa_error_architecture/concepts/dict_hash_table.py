"""Event indexes modeled as Python dictionaries.

Underlying data structure: dictionaries are open-addressed hash tables. Average
lookup, insert, and update are O(1), with O(n) worst case under extreme collision
patterns. Building an index over n events costs O(n) time and O(n) space, while
source indexes also store list references for grouped scans.
"""

from __future__ import annotations


def build_id_index(events: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    """Build an event_id -> event mapping in O(n) time and O(n) space."""
    return {str(event["event_id"]): event for event in events}


def build_source_index(events: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    """Group events by source, preserving input order within each source."""
    index: dict[str, list[dict[str, object]]] = {}
    for event in events:
        source = str(event["source"])
        index.setdefault(source, []).append(event)
    return index


def lookup_event(index: dict[str, dict[str, object]], event_id: str) -> dict[str, object] | None:
    """Return an event by id using average O(1) dict get."""
    return index.get(event_id)
