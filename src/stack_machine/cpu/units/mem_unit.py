from typing import List


class MemUnit:
    def __init__(self, cpu):  # type: ignore
        self.cpu = cpu

        self.need_mem = [0]
        self.write_read = [1]

    def handle(self, signal: List[str]) -> None:
        if self.cpu.simd_type == 1:
            if "write" in signal:
                addr = self.cpu.last_alu_output
                val = self.cpu.vector_stack.pop()
                self.cpu.mem.write(addr, val[0])
                self.cpu.mem.write(addr + 4, val[1])
                self.cpu.mem.write(addr + 8, val[2])
                self.cpu.mem.write(addr + 12, val[3])

            elif "read" in signal:
                addr = self.cpu.last_alu_output
                val1 = self.cpu.mem.read(addr)
                val2 = self.cpu.mem.read(addr + 4)
                val3 = self.cpu.mem.read(addr + 8)
                val4 = self.cpu.mem.read(addr + 12)
                self.cpu.vector_stack.push([val1, val2, val3, val4])

        else:
            if "write" in signal:
                addr = self.cpu.last_alu_output
                val = self.cpu.data_stack.pop()
                self.cpu.mem.write(addr, val)
            if "read" in signal:
                addr = self.cpu.last_alu_output
                val = self.cpu.mem.read(addr)
                self.cpu.data_stack.push(val)
