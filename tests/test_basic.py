import unittest
from Z80emulator import Z80emulator as Z80emu

class TestBasicCompiler(unittest.TestCase):
    def setUp(self):
        # CPU とメモリ初期化
        self.cpu = Z80emu["CPU"]()
        self.mem = Z80emu["Memory"]()
        self.cpu.memory = self.mem
        # BASIC コンパイラ
        self.basic = Z80emu["BasicCompiler"]()

    def test_let_and_halt(self):
        """LET と END(HALT) の動作テスト"""
        basic_code = [
            "LET A = 42",
            "END"
        ]
        bytecode = self.basic.compile(basic_code)

        # メモリにロード
        for addr, b in enumerate(bytecode):
            self.mem.write(addr, b)

        # CPU 実行
        while not self.cpu.halted:
            self.cpu.step()

        self.assertEqual(self.cpu.reg['A'], 42)

    def test_goto(self):
        """GOTO の動作テスト"""
        basic_code = [
            "LET A = 1",
            "GOTO skip",
            "LET A = 2",
            "skip: END"
        ]
        bytecode = self.basic.compile(basic_code)
        for addr, b in enumerate(bytecode):
            self.mem.write(addr, b)

        while not self.cpu.halted:
            self.cpu.step()

        # GOTO により LET A=2 はスキップ
        self.assertEqual(self.cpu.reg['A'], 1)

    def test_if_then(self):
        """IF ... THEN GOTO の動作テスト"""
        basic_code = [
            "LET A = 0",
            "IF A = 0 THEN GOTO skip",
            "LET A = 1",
            "skip: END"
        ]
        bytecode = self.basic.compile(basic_code)
        for addr, b in enumerate(bytecode):
            self.mem.write(addr, b)

        while not self.cpu.halted:
            self.cpu.step()

        # 条件により LET A=1 はスキップ
        self.assertEqual(self.cpu.reg['A'], 0)

if __name__ == "__main__":
    unittest.main()
