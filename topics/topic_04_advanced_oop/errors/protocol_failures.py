"""Runtime protocol validation helpers."""
from topics.topic_04_advanced_oop.concepts.abcs_protocols import ProcessorProtocol

def ensure_protocol_processor(obj):
    if not isinstance(obj, ProcessorProtocol):
        raise TypeError("object does not satisfy ProcessorProtocol")
    return obj
