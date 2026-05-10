"""Advanced solution for Topic 10."""
from topics.topic_10_network_sockets_protocols.concepts.protocol_design import validate_message
from topics.topic_10_network_sockets_protocols.dsa.udp_deduplicator import UdpDeduplicator

def ingest_protocol_messages(messages):
    dedupe = UdpDeduplicator(); accepted=[]; rejected=[]
    for position, message in enumerate(messages):
        try:
            validate_message(message)
            payload = message.get("payload", {})
            event_id = payload["event_id"]
            if dedupe.accept(event_id): accepted.append(payload)
            else: rejected.append({"position": position, "error_type": "duplicate"})
        except (KeyError, TypeError, ValueError) as exc:
            rejected.append({"position": position, "error_type": type(exc).__name__, "error": str(exc)})
    return {"events": tuple(accepted), "rejected": tuple(rejected), "seen": len(dedupe)}
