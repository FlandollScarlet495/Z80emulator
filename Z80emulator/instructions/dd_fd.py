class DD_FDInstructions:
    """
    DD (0xDD) = IX プレフィックス
    FD (0xFD) = IY プレフィックス
    IX/IY 専用命令の実行
    """

    @staticmethod
    def execute(cpu, prefix, opcode):
        reg_name = 'IX' if prefix == 0xDD else 'IY'
        reg = cpu.IX if reg_name == 'IX' else cpu.IY

        def get_hl_val():
            return (cpu.reg['H'] << 8) | cpu.reg['L']

        def set_hl_val(val):
            cpu.reg['H'] = (val >> 8) & 0xFF
            cpu.reg['L'] = val & 0xFF

        # --- LD r,(IX+d) / LD (IX+d),r ---
        if opcode in range(0x70, 0x78):  # LD (IX+d), r
            d = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            r = ['B','C','D','E','H','L','(HL)','A'][opcode-0x70]
            if r == '(HL)':
                val = cpu.memory.read(get_hl_val())
                cpu.memory.write((reg + d) & 0xFFFF, val)
            else:
                val = cpu.reg[r]
                cpu.memory.write((reg + d) & 0xFFFF, val)
        elif opcode in range(0x46, 0x4E+1, 8):  # LD r,(IX+d)
            d = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            r_list = ['B','C','D','E','H','L','(HL)','A']
            r = r_list[(opcode-0x40)//8]
            val = cpu.memory.read((reg + d) & 0xFFFF)
            cpu.reg[r] = val

        # --- INC/DEC (IX+d) ---
        elif opcode == 0x34:  # INC (IX+d)
            d = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            addr = (reg + d) & 0xFFFF
            val = (cpu.memory.read(addr) + 1) & 0xFF
            cpu.memory.write(addr, val)
        elif opcode == 0x35:  # DEC (IX+d)
            d = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            addr = (reg + d) & 0xFFFF
            val = (cpu.memory.read(addr) - 1) & 0xFF
            cpu.memory.write(addr, val)

        # --- ADD/ADC/SUB/SBC HL,IX/IY ---
        elif opcode == 0x09:  # ADD HL,IX/IY
            hl = get_hl_val()
            result = (hl + reg) & 0xFFFF
            set_hl_val(result)
        elif opcode == 0xDD or opcode == 0xFD:
            pass  # 他の16ビット演算はED/その他と組み合わせる

        # --- CBプレフィックス命令 (DD CB / FD CB) ---
        elif opcode == 0xCB:
            d = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            cb_opcode = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            addr = (reg + d) & 0xFFFF
            val = cpu.memory.read(addr)

            # RLC (IX+d)
            if cb_opcode == 0x00:
                val = ((val << 1) | (val >> 7)) & 0xFF
                cpu.memory.write(addr, val)
            # RRC (IX+d)
            elif cb_opcode == 0x08:
                val = ((val >> 1) | ((val & 1) << 7)) & 0xFF
                cpu.memory.write(addr, val)
            # BIT 0,(IX+d)
            elif cb_opcode == 0x40:
                cpu.flags['Z'] = 0 if (val & 0x01) else 1
            # 他のCB命令も同様に追加可能

        else:
            # 未対応命令はHALTで停止
            cpu.halted = True
