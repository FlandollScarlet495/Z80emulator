from .instr import Instructions
from ..memory import Memory
from ..flags import Flags

class BaseInstructions:
    memory: Memory
    reg: dict
    flags: Flags
    PC: int
    halted: bool

    def execute(self, opcode: int):
        Instructions.execute(self, opcode)
