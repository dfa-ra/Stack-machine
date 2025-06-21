import struct
from typing import List, Dict

import yaml  # type: ignore

from src.stack_machine.config import microcode_mem_file, op_table_file
from src.stack_machine.cpu.micro_command.micro_command_description import mc_sigs_info


class MicroCommand:
    def __init__(self) -> None:
        self.microcode_mem_path: str = microcode_mem_file
        self.op_table_path: str = op_table_file

        self.op_table = self.load_opcode_table()
        self.binary = self.load_binary_file()

    def load_binary_file(self) -> List[int]:
        with open(self.microcode_mem_path, "rb") as microcode_mem_f:
            data = microcode_mem_f.read()
        return list(struct.unpack("<" + "I" * (len(data) // 4), data))

    def load_opcode_table(self) -> Dict[int, int]:
        with open(self.op_table_path, "r") as op_table_f:
            content = yaml.safe_load(op_table_f)
        return content["op_table"]  # type: ignore

    def decode_mc_word(self, word: int) -> Dict[str, List[str]]:
        signals: Dict[str, List[str]] = {}
        for unit, desc in mc_sigs_info.items():
            start_bit = desc.bit_range[0]
            for name, bit_offset in desc.signals.items():
                bit_index = start_bit + bit_offset
                if (word >> bit_index) & 1:
                    if unit not in signals.keys():
                        signals[unit] = []
                    signals[unit].append(name)
        return signals

    def decode_microcode(self, op_code: int) -> list[dict[str, list[str]]]:
        if op_code not in self.op_table:
            raise ValueError(f"Unknown opcode: {op_code}")

        addr = self.op_table[op_code]
        decoded = []

        while True:
            word = self.binary[addr]
            decoded.append(self.decode_mc_word(word))
            if (word >> 31) & 1:  # term_mc
                decoded.pop()
                break
            addr += 1

        return decoded
