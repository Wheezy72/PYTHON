"""Entry solution for Topic 10."""
from topics.topic_10_network_sockets_protocols.concepts.framing import encode_frame, decode_frame

def round_trip_event(event):
    return decode_frame(encode_frame(event))
