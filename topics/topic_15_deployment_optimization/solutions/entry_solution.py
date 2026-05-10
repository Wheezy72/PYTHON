"""Entry solution for Topic 15."""
from topics.topic_15_deployment_optimization.concepts.bytecode import opcode_names

def inspect_transform(func):
    return {"opcodes": opcode_names(func), "opcode_count": len(opcode_names(func))}
