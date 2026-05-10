"""Bytecode inspection."""
import dis

def opcode_names(func):
    return tuple(instr.opname for instr in dis.get_instructions(func))
