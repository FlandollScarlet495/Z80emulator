class EDInstructions:
    """
    ED プレフィックス命令
    IN/OUT, LDI/LDD, CPI/CPD, ADC HL/ SBC HL, RETI/RETN などを処理
    """

    @staticmethod
    def execute(cpu, opcode):
        # --- 16ビット加算・減算 ---
        if opcode == 0x4A:  # ADC HL,BC
            hl = (cpu.reg['H'] << 8) | cpu.reg['L']
            bc = (cpu.reg['B'] << 8) | cpu.reg['C']
            carry = 1 if cpu.flags['C'] else 0
            result = (hl + bc + carry) & 0xFFFF
            cpu.reg['H'], cpu.reg['L'] = result >> 8, result & 0xFF
        elif opcode == 0x42:  # SBC HL,BC
            hl = (cpu.reg['H'] << 8) | cpu.reg['L']
            bc = (cpu.reg['B'] << 8) | cpu.reg['C']
            carry = 1 if cpu.flags['C'] else 0
            result = (hl - bc - carry) & 0xFFFF
            cpu.reg['H'], cpu.reg['L'] = result >> 8, result & 0xFF

        # --- LDI / LDD ---
        elif opcode == 0xA0:  # LDI
            hl = (cpu.reg['H'] << 8) | cpu.reg['L']
            de = (cpu.reg['D'] << 8) | cpu.reg['E']
            val = cpu.memory.read(hl)
            cpu.memory.write(de, val)
            hl += 1
            de += 1
            bc = (cpu.reg['B'] << 8) | cpu.reg['C']
            bc -= 1
            cpu.reg['H'], cpu.reg['L'] = hl >> 8, hl & 0xFF
            cpu.reg['D'], cpu.reg['E'] = de >> 8, de & 0xFF
            cpu.reg['B'], cpu.reg['C'] = bc >> 8, bc & 0xFF

        elif opcode == 0xA8:  # LDD
            hl = (cpu.reg['H'] << 8) | cpu.reg['L']
            de = (cpu.reg['D'] << 8) | cpu.reg['E']
            val = cpu.memory.read(hl)
            cpu.memory.write(de, val)
            hl -= 1
            de -= 1
            bc = (cpu.reg['B'] << 8) | cpu.reg['C']
            bc -= 1
            cpu.reg['H'], cpu.reg['L'] = hl >> 8, hl & 0xFF
            cpu.reg['D'], cpu.reg['E'] = de >> 8, de & 0xFF
            cpu.reg['B'], cpu.reg['C'] = bc >> 8, bc & 0xFF

        # --- CPI / CPD ---
        elif opcode == 0xA1:  # CPI
            hl = (cpu.reg['H'] << 8) | cpu.reg['L']
            val = cpu.memory.read(hl)
            cpu.flags['Z'] = 1 if cpu.reg['A'] == val else 0
            hl += 1
            bc = (cpu.reg['B'] << 8) | cpu.reg['C']
            bc -= 1
            cpu.reg['H'], cpu.reg['L'] = hl >> 8, hl & 0xFF
            cpu.reg['B'], cpu.reg['C'] = bc >> 8, bc & 0xFF

        elif opcode == 0xA9:  # CPD
            hl = (cpu.reg['H'] << 8) | cpu.reg['L']
            val = cpu.memory.read(hl)
            cpu.flags['Z'] = 1 if cpu.reg['A'] == val else 0
            hl -= 1
            bc = (cpu.reg['B'] << 8) | cpu.reg['C']
            bc -= 1
            cpu.reg['H'], cpu.reg['L'] = hl >> 8, hl & 0xFF
            cpu.reg['B'], cpu.reg['C'] = bc >> 8, bc & 0xFF

        # --- RETI / RETN ---
        elif opcode == 0x4D:  # RETI
            low = cpu.memory.read(cpu.SP)
            high = cpu.memory.read(cpu.SP + 1)
            cpu.SP += 2
            cpu.PC = (high << 8) | low
            # 割り込みフラグ処理は省略

        elif opcode == 0x45:  # RETN
            low = cpu.memory.read(cpu.SP)
            high = cpu.memory.read(cpu.SP + 1)
            cpu.SP += 2
            cpu.PC = (high << 8) | low
            # 割り込みフラグ復帰処理は省略

        # --- IN r,(C) / OUT (C),r ---
        elif opcode == 0x78:  # IN A,(C)
            port = (cpu.reg['B'] << 8) | cpu.reg['C']
            cpu.reg['A'] = cpu.io_read(port)
        elif opcode == 0x79:  # OUT (C),A
            port = (cpu.reg['B'] << 8) | cpu.reg['C']
            cpu.io_write(port, cpu.reg['A'])

        # --- 未対応命令は HALT ---
        else:
            cpu.halted = True
