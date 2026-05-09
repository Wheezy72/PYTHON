"""Set membership patterns for SentinelFlow tags and event ids.

Python sets and frozensets are hash tables. Membership checks, insertions, and
deduplication are O(1) average per item, with O(n) worst case under pathological
hash collisions. For SentinelFlow tag filters, normalizing t input tags costs
O(t) time and O(u) space, where u is the number of unique stripped tags.

Filtering n events by r required tags normalizes each event tag collection once.
The total cost is O(n*t + r) time, where t is the average tag count per event,
and O(t + r) temporary space per scanned event.
"""

from __future__ import annotations

from collections.abc import Iterable


def normalize_tag_set(tags) -> frozenset[str]:
    """Strip, validate, and deduplicate tags into a frozenset."""
    if isinstance(tags, (str, bytes)):
        raise TypeError("tags must be an iterable of strings, not a string")
    try:
        iterator = iter(tags)
    except TypeError as exc:
        raise TypeError("tags must be iterable") from exc

    normalized: set[str] = set()
    for tag in iterator:
        if not isinstance(tag, str):
            raise TypeError("tags must contain only strings")
        text = tag.strip()
        if not text:
            raise ValueError("tags must contain only non-blank strings")
        normalized.add(text)
    return frozenset(normalized)


def unique_tags(events) -> set[str]:
    """Return all unique normalized tags from event dictionaries."""
    unique: set[str] = set()
    for event in events:
        tags = event["tags"]
        if not isinstance(tags, (list, tuple, set, frozenset)):
            raise TypeError("event tags must be a list, tuple, set, or frozenset")
        unique.update(normalize_tag_set(tags))
    return unique


def events_matching_all_tags(events, required_tags) -> list[dict[str, object]]:
    """Return events whose normalized tag set includes every required tag."""
    required = normalize_tag_set(required_tags)
    matches: list[dict[str, object]] = []
    for event in events:
        tags = event["tags"]
        if not isinstance(tags, (list, tuple, set, frozenset)):
            raise TypeError("event tags must be a list, tuple, set, or frozenset")
        event_tags = normalize_tag_set(tags)
        if event_tags.issuperset(required):
            matches.append(event)
    return matches


def unique_event_ids(event_ids: Iterable[str]) -> tuple[str, ...]:
    """Return event ids in first-seen order, dropping later duplicates."""
    seen: set[str] = set()
    unique: list[str] = []
    for event_id in event_ids:
        if event_id not in seen:
            seen.add(event_id)
            unique.append(event_id)
    return tuple(unique)


def find_duplicate_event_ids(event_ids: Iterable[str]) -> tuple[str, ...]:
    """Return duplicated event ids once, in first duplicate-seen order."""
    seen: set[str] = set()
    reported: set[str] = set()
    duplicates: list[str] = []
    for event_id in event_ids:
        if event_id in seen and event_id not in reported:
            duplicates.append(event_id)
            reported.add(event_id)
        else:
            seen.add(event_id)
    return tuple(duplicates)
