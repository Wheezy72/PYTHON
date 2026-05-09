# Mid Challenge: Tag Registry and Defensive Filtering

Build a hash-backed tag registry and filtering helper for SentinelFlow event records.

## Requirements

- Validate and normalize incoming records.
- Build a registry that maps each tag to the event ids that contain it.
- Build a reverse lookup from event id to its normalized tag set.
- Normalize tag whitespace and reject invalid tag types.
- Return immutable tag and event-id views.
- Filter records by a required tag set using average O(1) tag membership per tag.
- Keep both registry directions consistent if the same event id is added again.

## Complexity questions

- Why are set membership checks average O(1)?
- Why does building the registry cost O(n * t), where t is average tags per event?
- Why should defensive validation raise TypeError for wrong field types and ValueError for invalid values?
