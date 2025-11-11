from .cpu import CPU
from .memory import Memory
from .flags import Flags
from .assembler import Assembler
from .basic import BasicCompiler
from .instructions.instr import Instructions
from .instructions.jumps import JumpInstructions
from .instructions.cb import CBInstructions
from .instructions.ed import EDInstructions
from .instructions.dd_fd import DD_FDInstructions

Z80emulator = {
    "CPU": CPU,
    "Memory": Memory,
    "Flags": Flags,
    "Assembler": Assembler,
    "BasicCompiler": BasicCompiler,
    "Instructions": Instructions,
    "JumpInstructions": JumpInstructions,
    "CBInstructions": CBInstructions,
    "EDInstructions": EDInstructions,
    "DD_FDInstructions": DD_FDInstructions
}
