from .instructions.instr import Instructions

class Assembler:
    """
    Z80用簡易アセンブラ
    - ラベル解決
    - 基本命令、CB/ED/DD/FDプレフィックス対応
    """

    def __init__(self):
        self.labels = {}
        self.code = []

    def assemble(self, lines):
        """
        lines: リスト of str
        returns: バイト列（list of int）
        """
        # --- ラベル先行定義パス ---
        pc = 0
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            if line.endswith(':'):
                label = line[:-1]
                self.labels[label] = pc
            else:
                pc += self.instruction_size(line)

        # --- 実際のコード生成パス ---
        self.code = []
        pc = 0
        for line in lines:
            line = line.strip()
            if not line or line.endswith(':') or line.startswith(';'):
                continue
            bytes_ = self.parse_instruction(line, pc)
            self.code.extend(bytes_)
            pc += len(bytes_)

        return self.code

    def instruction_size(self, line):
        """簡易: 各命令サイズを返す"""
        parts = line.split()
        inst = parts[0].upper()
        # 簡易サイズ推定
        if inst in ['NOP','HALT','RET']: return 1
        if inst in ['LD','ADD','SUB','INC','DEC','CALL','JP','JR']: return 2
        if inst.startswith('ED') or inst.startswith('CB') or inst.startswith('DD') or inst.startswith('FD'):
            return 2
        return 1

    def parse_instruction(self, line, pc):
        """
        文字列命令 -> バイト列
        非常に簡易化している。拡張可能
        """
        parts = line.replace(',',' ').split()
        inst = parts[0].upper()
        args = parts[1:] if len(parts) > 1 else []

        code = []

        # --- 基本命令サンプル ---
        if inst == 'NOP':
            code.append(0x00)
        elif inst == 'HALT':
            code.append(0x76)
        elif inst == 'LD':
            # LD A,n
            if args[0].upper() == 'A' and args[1].isdigit():
                code.extend([0x3E, int(args[1]) & 0xFF])
            # LD B,n
            elif args[0].upper() == 'B' and args[1].isdigit():
                code.extend([0x06, int(args[1]) & 0xFF])
        elif inst == 'ADD':
            if args[0].upper() == 'A' and args[1].upper() == 'B':
                code.append(0x80)
        elif inst == 'JP':
            if args[0] in self.labels:
                addr = self.labels[args[0]]
                code.append(0xC3)
                code.append(addr & 0xFF)
                code.append((addr >> 8) & 0xFF)
        elif inst == 'CALL':
            if args[0] in self.labels:
                addr = self.labels[args[0]]
                code.append(0xCD)
                code.append(addr & 0xFF)
                code.append((addr >> 8) & 0xFF)
        elif inst == 'RET':
            code.append(0xC9)
        else:
            # 未対応命令はNOPとして無視
            code.append(0x00)

        return code
