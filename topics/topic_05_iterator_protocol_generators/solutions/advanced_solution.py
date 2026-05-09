"""Advanced solution for Topic 05."""
from topics.topic_05_iterator_protocol_generators.concepts.batching_backpressure import batches
from topics.topic_05_iterator_protocol_generators.solutions.mid_solution import normalize_messages, stream_alerts

def run_streaming_ingestion(events, minimum=4, batch_size=2):
    normalized = normalize_messages(events)
    alerts = stream_alerts(normalized, minimum)
    return {"batches": tuple(batches(alerts, batch_size))}
