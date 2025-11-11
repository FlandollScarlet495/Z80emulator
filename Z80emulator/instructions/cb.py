class CBInstructions:
    """
    CB プレフィックス命令
    RLC/RRC/RL/RR/SLA/SRA/SRL/BIT/SET/RES 命令を処理
    対応レジスタ: B,C,D,E,H,L,A, (HL)
    """

    @staticmethod
    def execute(cpu, opcode):
        reg_map = ['B','C','D','E','H','L','(HL)','A']

        def get_reg_val(r):
            if r == '(HL)':
                addr = (cpu.reg['H'] << 8) | cpu.reg['L']
                return cpu.memory.read(addr)
            else:
                return cpu.reg[r]

        def set_reg_val(r, val):
            val &= 0xFF
            if r == '(HL)':
                addr = (cpu.reg['H'] << 8) | cpu.reg['L']
                cpu.memory.write(addr, val)
            else:
                cpu.reg[r] = val

        # RLC r (0x00-0x07)
        if 0x00 <= opcode <= 0x07:
            r = reg_map[opcode & 0x07]
            val = get_reg_val(r)
            result = ((val << 1) | (val >> 7)) & 0xFF
            set_reg_val(r, result)
            cpu.flags['Z'] = 1 if result == 0 else 0

        # RRC r (0x08-0x0F)
        elif 0x08 <= opcode <= 0x0F:
            r = reg_map[opcode & 0x07]
            val = get_reg_val(r)
            result = ((val >> 1) | ((val & 1) << 7)) & 0xFF
            set_reg_val(r, result)
            cpu.flags['Z'] = 1 if result == 0 else 0

        # RL r (0x10-0x17)
        elif 0x10 <= opcode <= 0x17:
            r = reg_map[opcode & 0x07]
            val = get_reg_val(r)
            carry = 1 if cpu.flags['C'] else 0
            result = ((val << 1) | carry) & 0xFF
            cpu.flags['C'] = (val >> 7) & 1
            set_reg_val(r, result)
            cpu.flags['Z'] = 1 if result == 0 else 0

        # RR r (0x18-0x1F)
        elif 0x18 <= opcode <= 0x1F:
            r = reg_map[opcode & 0x07]
            val = get_reg_val(r)
            carry = 1 if cpu.flags['C'] else 0
            result = ((carry << 7) | (val >> 1)) & 0xFF
            cpu.flags['C'] = val & 1
            set_reg_val(r, result)
            cpu.flags['Z'] = 1 if result == 0 else 0

        # SLA r (0x20-0x27)
        elif 0x20 <= opcode <= 0x27:
            r = reg_map[opcode & 0x07]
            val = get_reg_val(r)
            cpu.flags['C'] = (val >> 7) & 1
            set_reg_val(r, (val << 1) & 0xFF)
            cpu.flags['Z'] = 1 if get_reg_val(r) == 0 else 0

        # SRA r (0x28-0x2F)
        elif 0x28 <= opcode <= 0x2F:
            r = reg_map[opcode & 0x07]
            val = get_reg_val(r)
            msb = val & 0x80
            cpu.flags['C'] = val & 1
            set_reg_val(r, ((val >> 1) | msb) & 0xFF)
            cpu.flags['Z'] = 1 if get_reg_val(r) == 0 else 0

        # SRL r (0x38-0x3F)
        elif 0x38 <= opcode <= 0x3F:
            r = reg_map[opcode & 0x07]
            val = get_reg_val(r)
            cpu.flags['C'] = val & 1
            set_reg_val(r, (val >> 1) & 0xFF)
            cpu.flags['Z'] = 1 if get_reg_val(r) == 0 else 0

        # BIT b,r (0x40-0x7F)
        elif 0x40 <= opcode <= 0x7F:
            bit = (opcode >> 3) & 0x07
            r = reg_map[opcode & 0x07]
            val = get_reg_val(r)
            cpu.flags['Z'] = 0 if (val & (1 << bit)) else 1

        # RES b,r (0x80-0xBF)
        elif 0x80 <= opcode <= 0xBF:
            bit = (opcode >> 3) & 0x07
            r = reg_map[opcode & 0x07]
            val = get_reg_val(r)
            val &= ~(1 << bit)
            set_reg_val(r, val)

        # SET b,r (0xC0-0xFF)
        elif 0xC0 <= opcode <= 0xFF:
            bit = (opcode >> 3) & 0x07
            r = reg_map[opcode & 0x07]
            val = get_reg_val(r)
            val |= (1 << bit)
            set_reg_val(r, val)

        else:
            cpu.halted = True
