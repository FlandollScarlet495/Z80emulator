class Memory:
    def __init__(self, size: int = 0x10000):
        self.mem = [0] * size

    def read(self, addr: int) -> int:
        return self.mem[addr & 0xFFFF]

    def write(self, addr: int, val: int):
        self.mem[addr & 0xFFFF] = val & 0xFF
