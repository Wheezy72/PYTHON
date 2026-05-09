"""Big O tradeoffs for linear SentinelFlow data structures.

Lists, dictionaries, sets, and deques optimize different access patterns. Lists
are compact dynamic arrays for ordered scans. Dicts and sets spend extra table
space to provide average O(1) hashing operations. Deques trade random access for
stable O(1) FIFO operations at both ends.
"""

from __future__ import annotations


def complexity_table() -> dict[str, dict[str, str]]:
    """Return a compact complexity summary for Topic 02 structures."""
    return {
        "list": {"append": "O(1) amortized", "index": "O(1)", "scan": "O(n)", "space": "O(n)"},
        "dict": {"lookup": "O(1) average", "insert": "O(1) average", "scan": "O(n)", "space": "O(n)"},
        "set": {"membership": "O(1) average", "insert": "O(1) average", "scan": "O(n)", "space": "O(n)"},
        "deque": {"enqueue": "O(1)", "dequeue": "O(1)", "index": "O(n)", "space": "O(n)"},
    }


def recommend_structure(access_pattern: str) -> str:
    """Map a common access pattern to the best Topic 02 structure."""
    recommendations = {
        "ordered_scan": "list",
        "id_lookup": "dict",
        "tag_membership": "set",
        "fifo": "deque",
    }
    return recommendations.get(access_pattern, "list")
