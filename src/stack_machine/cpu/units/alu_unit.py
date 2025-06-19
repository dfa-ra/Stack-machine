from typing import List


class ALU:
    def __init__(self, cpu) -> None:  # type: ignore

        self.right: int = 0
        self.left: int = 0
        self.cpu = cpu
        # по аналогии можешь добавить
        self.open_a = [0]
        self.open_b = [1]
        self.add = [2]
        self.sub = [3]
        self.and_ = [4]
        self.or_ = [5]

        self.alu_output = 0

    def handle(self, signal: List[str], left: int, right: int) -> int:
        self.init_operands(left, right)
        self.arithmetic_logic(signal)
        return self.alu_output

    def init_operands(self, left: int = 0, right: int = 0) -> None:
        self.left = left
        self.right = right

    def arithmetic_logic(self, signal: List[str]) -> None:
        if "add" in signal:
            if "if" in signal:
                if self.cpu.data_stack.get_T() != 0:
                    self.alu_output = self.left
                else:
                    self.alu_output = self.left + self.right
            elif "-if" in signal:
                if self.cpu.data_stack.get_T() < 0:
                    self.alu_output = self.left
                else:
                    self.alu_output = self.left + self.right
            else:
                self.alu_output = self.left + self.right
        elif "sub" in signal:
            self.alu_output = self.left - self.right
        elif "and" in signal:
            self.alu_output = self.left & self.right
        elif "or" in signal:
            self.alu_output = self.left | self.right
        elif "inc" in signal:
            self.alu_output = self.left + 1
        elif "mul" in signal:
            self.alu_output = self.left * self.right
        elif "div" in signal:
            self.alu_output = self.left // self.right
        elif "shl" in signal:
            self.alu_output = self.left << 1
        elif "shr" in signal:
            self.alu_output = self.left >> 1
        elif "not" in signal:
            self.alu_output = ~self.left
        elif "xor" in signal:
            self.alu_output = self.left ^ self.right
