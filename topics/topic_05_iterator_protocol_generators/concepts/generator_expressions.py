"""Generator expression helpers."""
def high_severity_ids(events, minimum):
    return (event["event_id"] for event in events if event["severity"] >= minimum)
