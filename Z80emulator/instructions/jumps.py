class JumpInstructions:
    """
    Z80 ジャンプ・CALL・RET・PUSH/POP 命令
    条件付きジャンプ、無条件ジャンプ、CALL/RET、PUSH/POP を処理
    """

    @staticmethod
    def execute(cpu, opcode):
        # --- 条件判定ヘルパー ---
        def check_condition(cond):
            if cond == 'NZ': return cpu.flags['Z'] == 0
            if cond == 'Z':  return cpu.flags['Z'] == 1
            if cond == 'NC': return cpu.flags['C'] == 0
            if cond == 'C':  return cpu.flags['C'] == 1
            if cond == 'PO': return cpu.flags.get('P', 0) == 0
            if cond == 'PE': return cpu.flags.get('P', 0) == 1
            if cond == 'P':  return cpu.flags.get('S', 0) == 0
            if cond == 'M':  return cpu.flags.get('S', 0) == 1
            return False

        # --- JP nn ---
        if opcode == 0xC3:
            low = cpu.memory.read(cpu.PC)
            high = cpu.memory.read(cpu.PC+1)
            cpu.PC = (high << 8) | low

        # --- JP cc,nn ---
        elif opcode in [0xC2,0xCA,0xD2,0xDA,0xE2,0xEA,0xF2,0xFA]:
            cc_map = {0xC2:'NZ', 0xCA:'Z', 0xD2:'NC', 0xDA:'C',
                      0xE2:'PO', 0xEA:'PE', 0xF2:'P', 0xFA:'M'}
            low = cpu.memory.read(cpu.PC)
            high = cpu.memory.read(cpu.PC+1)
            addr = (high << 8) | low
            cpu.PC += 2
            if check_condition(cc_map[opcode]):
                cpu.PC = addr

        # --- JR e ---
        elif opcode == 0x18:
            offset = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            if offset & 0x80:
                offset -= 0x100
            cpu.PC = (cpu.PC + offset) & 0xFFFF

        # --- JR cc,e ---
        elif opcode in [0x20,0x28,0x30,0x38]:
            cc_map = {0x20:'NZ', 0x28:'Z', 0x30:'NC', 0x38:'C'}
            offset = cpu.memory.read(cpu.PC)
            cpu.PC += 1
            if offset & 0x80:
                offset -= 0x100
            if check_condition(cc_map[opcode]):
                cpu.PC = (cpu.PC + offset) & 0xFFFF

        # --- CALL nn ---
        elif opcode == 0xCD:
            low = cpu.memory.read(cpu.PC)
            high = cpu.memory.read(cpu.PC+1)
            addr = (high << 8) | low
            cpu.PC += 2
            cpu.SP -= 2
            cpu.memory.write(cpu.SP, cpu.PC & 0xFF)
            cpu.memory.write(cpu.SP+1, cpu.PC >> 8)
            cpu.PC = addr

        # --- CALL cc,nn ---
        elif opcode in [0xC4,0xCC,0xD4,0xDC,0xE4,0xEC,0xF4,0xFC]:
            cc_map = {0xC4:'NZ', 0xCC:'Z', 0xD4:'NC', 0xDC:'C',
                      0xE4:'PO', 0xEC:'PE', 0xF4:'P', 0xFC:'M'}
            low = cpu.memory.read(cpu.PC)
            high = cpu.memory.read(cpu.PC+1)
            addr = (high << 8) | low
            cpu.PC += 2
            if check_condition(cc_map[opcode]):
                cpu.SP -= 2
                cpu.memory.write(cpu.SP, cpu.PC & 0xFF)
                cpu.memory.write(cpu.SP+1, cpu.PC >> 8)
                cpu.PC = addr

        # --- RET ---
        elif opcode == 0xC9:
            low = cpu.memory.read(cpu.SP)
            high = cpu.memory.read(cpu.SP+1)
            cpu.SP += 2
            cpu.PC = (high << 8) | low

        # --- RET cc ---
        elif opcode in [0xC0,0xC8,0xD0,0xD8,0xE0,0xE8,0xF0,0xF8]:
            cc_map = {0xC0:'NZ', 0xC8:'Z', 0xD0:'NC', 0xD8:'C',
                      0xE0:'PO', 0xE8:'PE', 0xF0:'P', 0xF8:'M'}
            if check_condition(cc_map[opcode]):
                low = cpu.memory.read(cpu.SP)
                high = cpu.memory.read(cpu.SP+1)
                cpu.SP += 2
                cpu.PC = (high << 8) | low

        # --- PUSH rr ---
        elif opcode in [0xC5,0xD5,0xE5,0xF5]:  # BC,DE,HL,AF
            rr_map = {0xC5:('B','C'), 0xD5:('D','E'), 0xE5:('H','L'), 0xF5:('A','F')}
            r1,r2 = rr_map[opcode]
            cpu.SP -= 2
            cpu.memory.write(cpu.SP, cpu.reg[r2])
            cpu.memory.write(cpu.SP+1, cpu.reg[r1])

        # --- POP rr ---
        elif opcode in [0xC1,0xD1,0xE1,0xF1]:  # BC,DE,HL,AF
            rr_map = {0xC1:('B','C'), 0xD1:('D','E'), 0xE1:('H','L'), 0xF1:('A','F')}
            r1,r2 = rr_map[opcode]
            cpu.reg[r1] = cpu.memory.read(cpu.SP+1)
            cpu.reg[r2] = cpu.memory.read(cpu.SP)
            cpu.SP += 2

        else:
            # 未対応命令は HALT
            cpu.halted = True
