"""Generator basics for SentinelFlow."""
def event_ids(events):
    for event in events:
        yield event["event_id"]

def chain_sources(*sources):
    for source in sources:
        yield from source
