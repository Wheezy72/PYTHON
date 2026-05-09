"""TypeError and ValueError boundaries for hash-backed tag sets.

Set membership requires hashable objects and averages O(1) per insertion. This
module narrows SentinelFlow tags to non-blank strings, raising TypeError for
wrong tag types and ValueError for strings that contain no usable content.
"""

from __future__ import annotations


def ensure_hashable_tag(tag) -> str:
    """Validate one tag as a non-blank string suitable for set membership."""
    if not isinstance(tag, str):
        raise TypeError("tag must be a string")
    text = tag.strip()
    if not text:
        raise ValueError("tag must be non-blank")
    return text


def build_tag_membership(tags) -> set[str]:
    """Validate tags and return a set in O(n) average time and O(n) space."""
    return {ensure_hashable_tag(tag) for tag in tags}
