from Z80emulator.assembler import Assembler

class BasicCompiler:
    """
    Visual Basic風命令 -> Z80マシン語
    対応:
        - LET A = 10
        - PRINT A
        - GOTO label
        - IF A = 0 THEN GOTO label
        - END
    """

    def __init__(self):
        self.assembler = Assembler()
        self.labels = {}

    def compile(self, lines):
        """
        lines: BASICソースコード (list of str)
        returns: バイト列 (list of int)
        """
        asm_lines = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith("'"):
                continue  # コメント

            # ラベル定義
            if ':' in line:
                label, stmt = line.split(':',1)
                label = label.strip()
                stmt = stmt.strip()
                self.labels[label] = len(asm_lines)
                line = stmt

            # LET A = n
            if line.upper().startswith('LET'):
                parts = line[3:].split('=')
                reg = parts[0].strip().upper()
                val = int(parts[1].strip())
                asm_lines.append(f"LD {reg},{val}")

            # PRINT A -> LD A,n + OUT (C),A として簡易化
            elif line.upper().startswith('PRINT'):
                reg = line[5:].strip().upper()
                # 仮にAレジスタからI/Oポート0に出力する形式
                asm_lines.append(f"LD A,{reg}")  # 簡易サンプル

            # GOTO label
            elif line.upper().startswith('GOTO'):
                label = line[4:].strip()
                asm_lines.append(f"JP {label}")

            # IF A = 0 THEN GOTO label
            elif line.upper().startswith('IF'):
                cond_part = line[2:].strip()
                if 'THEN' in cond_part:
                    expr, then_part = cond_part.split('THEN',1)
                    expr = expr.strip()
                    then_part = then_part.strip()
                    # 簡易: A=0 なら JP
                    if '=' in expr:
                        reg, val = expr.split('=')
                        reg = reg.strip().upper()
                        val = int(val.strip())
                        # SUB val して Z フラグ設定
                        asm_lines.append(f"LD B,{val}")  # 仮にBに値ロード
                        asm_lines.append(f"SUB {reg},B")  # 仮想 SUB
                        target_label = then_part.split()[1]  # GOTOラベル
                        asm_lines.append(f"JP Z,{target_label}")

            # END -> HALT
            elif line.upper() == 'END':
                asm_lines.append("HALT")

        # Assemble BASIC -> Z80 マシン語
        bytecode = self.assembler.assemble(asm_lines)
        return bytecode
