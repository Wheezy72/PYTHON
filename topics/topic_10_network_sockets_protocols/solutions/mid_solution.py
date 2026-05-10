"""Mid solution for Topic 10."""
from topics.topic_10_network_sockets_protocols.concepts.framing import decode_frame
from topics.topic_10_network_sockets_protocols.dsa.protocol_buffer import ProtocolBuffer

def decode_stream(chunks):
    buffer = ProtocolBuffer(); events = []
    for chunk in chunks:
        buffer.feed(chunk)
        events.extend(decode_frame(frame) for frame in buffer.pop_frames())
    return tuple(events), len(buffer)
