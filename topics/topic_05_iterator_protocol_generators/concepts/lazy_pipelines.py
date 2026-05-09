"""Lazy map/filter helpers."""
def lazy_filter(events, predicate):
    for event in events:
        if predicate(event):
            yield event

def lazy_map(events, transform):
    for event in events:
        yield transform(event)
