class Instruction:
    def __init__(self, val: tuple[int, int]):
        self.mc_addr: int = val[0]
        self.imm: int | None = val[1] if val[1] is not None else None
        self.bits: int = (val[0] << 8) | (self.imm if self.imm is not None else 0)
