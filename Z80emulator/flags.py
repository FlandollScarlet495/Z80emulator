class Flags:
    S: int
    Z: int
    H: int
    P: int
    N: int
    C: int

    def __init__(self):
        self.S = 0
        self.Z = 0
        self.H = 0
        self.P = 0
        self.N = 0
        self.C = 0

    def update_add(self, a: int, b: int) -> int:
        res = a + b
        self.S = 1 if res & 0x80 else 0
        self.Z = 1 if (res & 0xFF) == 0 else 0
        self.H = 1 if (a & 0xF) + (b & 0xF) > 0xF else 0
        self.C = 1 if res > 0xFF else 0
        self.P = 1 if bin(res & 0xFF).count('1') % 2 == 0 else 0
        self.N = 0
        return res & 0xFF

    def update_sub(self, a: int, b: int) -> int:
        res = a - b
        self.S = 1 if res & 0x80 else 0
        self.Z = 1 if (res & 0xFF) == 0 else 0
        self.H = 1 if (a & 0xF) < (b & 0xF) else 0
        self.C = 1 if a < b else 0
        self.P = 1 if bin(res & 0xFF).count('1') % 2 == 0 else 0
        self.N = 1
        return res & 0xFF
