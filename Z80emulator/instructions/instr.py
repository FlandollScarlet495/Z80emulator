from .cb import CBInstructions
from .ed import EDInstructions
from .dd_fd import DD_FDInstructions
from .jumps import JumpInstructions

class Instructions:
    @staticmethod
    def execute(cpu, opcode: int):
        """
        opcodeに応じて各モジュールに振り分ける
        """
        if opcode == 0x00:
            pass  # NOP
        elif opcode == 0x76:
            cpu.halted = True  # HALT
        elif opcode == 0x3E:
            val = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            cpu.reg['A'] = val  # LD A,n
        elif opcode == 0x06:
            val = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            cpu.reg['B'] = val  # LD B,n
        elif opcode == 0x80:
            cpu.reg['A'] = (cpu.reg['A'] + cpu.reg['B']) & 0xFF  # ADD A,B
        elif opcode == 0xCB:
            cb_opcode = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            CBInstructions.execute(cpu, cb_opcode)
        elif opcode == 0xED:
            ed_opcode = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            EDInstructions.execute(cpu, ed_opcode)
        elif opcode in [0xDD, 0xFD]:
            ddfd_opcode = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            DD_FDInstructions.execute(cpu, opcode, ddfd_opcode)
        elif opcode >= 0xC0:
            JumpInstructions.execute(cpu, opcode)
        else:
            cpu.halted = True
