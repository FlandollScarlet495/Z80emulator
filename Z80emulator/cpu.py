from .memory import Memory
from .flags import Flags
from .instructions.base import BaseInstructions

class CPU(BaseInstructions):
    def __init__(self):
        self.reg = {'A':0,'B':0,'C':0,'D':0,'E':0,'H':0,'L':0}
        self.SP = 0xFFFE
        self.PC = 0
        self.IX = 0
        self.IY = 0
        self.flags = Flags()
        self.memory = Memory()
        self.halted = False

    def step(self):
        if self.halted:
            return
        opcode = self.memory.read(self.PC)
        self.PC += 1
        self.execute(opcode)

    def run(self, max_steps=100000):
        steps = 0
        while not self.halted and steps < max_steps:
            self.step()
            steps += 1
