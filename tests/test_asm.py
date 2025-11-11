import unittest
from Z80emulator import Z80emulator as Z80emu

class TestAssembler(unittest.TestCase):
    def setUp(self):
        self.cpu = Z80emu["CPU"]()
        self.mem = Z80emu["Memory"]()
        self.cpu.memory = self.mem
        self.assembler = Z80emu["Assembler"]()

    def test_ld_add_halt(self):
        """LD / ADD / HALT の動作テスト"""
        asm_lines = [
            "LD A,10",
            "LD B,20",
            "ADD A,B",
            "HALT"
        ]
        bytecode = self.assembler.assemble(asm_lines)

        # メモリにロード
        for addr, b in enumerate(bytecode):
            self.mem.write(addr, b)

        # CPU 実行
        while not self.cpu.halted:
            self.cpu.step()

        # Aレジスタ = 10 + 20
        self.assertEqual(self.cpu.reg['A'], 30)

    def test_label_and_jp(self):
        """ラベルと JP の動作テスト"""
        asm_lines = [
            "start:",
            "LD A,5",
            "JP end",
            "LD A,10",
            "end: HALT"
        ]
        bytecode = self.assembler.assemble(asm_lines)
        for addr, b in enumerate(bytecode):
            self.mem.write(addr, b)

        while not self.cpu.halted:
            self.cpu.step()

        # JP により LD A,10 はスキップ
        self.assertEqual(self.cpu.reg['A'], 5)

    def test_call_and_ret(self):
        """CALL / RET の動作テスト"""
        asm_lines = [
            "CALL sub",
            "HALT",
            "sub: LD A,99",
            "RET"
        ]
        bytecode = self.assembler.assemble(asm_lines)
        for addr, b in enumerate(bytecode):
            self.mem.write(addr, b)

        while not self.cpu.halted:
            self.cpu.step()

        self.assertEqual(self.cpu.reg['A'], 99)

if __name__ == "__main__":
    unittest.main()
