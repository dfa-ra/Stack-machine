from src.stack_machine.utils.bitwise_utils import btle, ltbe, tsfb


class DataMem:
    def __init__(
        self, io_addr: list[int], io_data: list[int], data_mem: bytearray
    ) -> None:
        # Читаем бинарный файл
        self.mem = data_mem
        self.size = len(data_mem)
        self.input = io_addr[0]
        self.output = io_addr[1]
        self.input_stream = io_data
        self.output_stream: list[int] = []


    def get_out(self) -> list[int]:
        return self.output_stream

    def get_in(self) -> list[int]:
        return self.input_stream

    def write(self, address: int, value: int) -> None:
        value = ltbe(value)
        if address <= self.size - 4:
            if address == self.output:
                self.output_stream.append(value)

            for i in range(4):
                self.mem[address + i] = (value >> (24 - i * 8)) & 0xFF
        else:
            raise ValueError("Attempting to write memory out of address space")

    def read(self, address: int) -> int:
        if address <= self.size - 4:
            if address == self.input:
                ret = self.input_stream[0]
                ret = ret & 0xFFFFFFFF
                self.input_stream.pop(0)

                return tsfb(ret)
            ret = 0
            for i in range(4):
                ret |= self.mem[address + i] << (24 - i * 8)
            return tsfb(btle(ret))
        else:
            raise ValueError("Attempting to read memory out of address space")
