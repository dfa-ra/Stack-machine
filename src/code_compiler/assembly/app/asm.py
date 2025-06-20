import os
import struct
from typing import Tuple, List, Dict

import yaml  # type: ignore

from src.stack_machine.config import instruction_file


def load_opcodes(yaml_file: str) -> Dict[str, List[str]]:
    try:
        with open(yaml_file, "r") as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
    except Exception as e:
        raise ValueError(f"Failed to load opcodes from {yaml_file}: {e}")
    opcodes = {}
    for cmd in data["commands"]:
        opcodes[cmd["desc"]] = [cmd["opcode"], cmd["operand"]]
    return opcodes


def convert_to_binary(build_dir: str, input_file: str, memory_size: int) -> None:
    os.makedirs(build_dir + "/bin", exist_ok=True)

    data_mem_path = build_dir + "/bin/data_memory.bin"
    instruction_mem_path = build_dir + "/bin/instruction_memory.bin"

    commands = load_opcodes(instruction_file)
    instructions: List[Tuple[str, int | None]] = []
    data_entries: List[Tuple[int, str, List[int]]] = []
    addr_set = set()

    current_section = None
    start_address = -1
    instruction_offset: int = 0

    with open(input_file, "r") as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("\\"):
                continue

            parts = line.split(";")[0].split()
            if not parts:
                continue

            if parts[0] == ".data":
                current_section = "data"
                continue
            elif parts[0] == ".text":
                current_section = "text"
                continue

            if current_section == "data":
                if len(parts) < 3 or parts[0] != "var":
                    raise ValueError(
                        f"Line {line_number}: Invalid .data format, expected 'VAR <addr> BYTE <value>...' or 'VAR <addr> WORD <value>'"
                    )
                try:
                    addr = int(parts[1], 0)
                    data_type = parts[2]
                    if data_type not in ("byte", "word"):
                        raise ValueError(
                            f"Line {line_number}: Invalid data type, expected 'BYTE' or 'WORD'"
                        )

                    if data_type == "word":
                        if len(parts) < 4:
                            raise ValueError(
                                f"Line {line_number}: VAR WORD expects exactly one value"
                            )
                        values = []
                        for val in parts[3:]:
                            v = int(val, 0)
                            v = v & 0xFFFFFFFF
                            if v < 0 or v > 0xFFFFFFFF:
                                raise ValueError(
                                    f"Line {line_number}: WORD value out of range (0 to 0xFFFFFFFF)"
                                )
                            values.append(v)
                        for i in range(addr, addr + len(values) * 4):
                            if i in addr_set:
                                raise ValueError(
                                    f"Line {line_number}: Address {i} overlaps with previously defined data"
                                )
                            addr_set.add(i)
                        data_entries.append((addr, "word", values))

                    elif data_type == "byte":
                        if len(parts) < 4:
                            raise ValueError(
                                f"Line {line_number}: VAR BYTE expects at least one value"
                            )
                        values = []
                        for val in parts[3:]:
                            v = int(val, 0)
                            if v < 0 or v > 255:
                                raise ValueError(
                                    f"Line {line_number}: BYTE value out of range (0 to 255)"
                                )
                            values.append(v)
                        for i in range(addr, addr + len(values)):
                            if i in addr_set:
                                raise ValueError(
                                    f"Line {line_number}: Address {i} overlaps with previously defined data"
                                )
                            addr_set.add(i)
                        data_entries.append((addr, "byte", values))

                except ValueError as e:
                    if str(e).startswith("Line"):
                        raise
                    raise ValueError(
                        f"Line {line_number}: Invalid address or value in .data"
                    )

            elif current_section == "text":
                if parts[0] == "_start":
                    if start_address != -1:
                        raise ValueError(
                            f"Line {line_number}: Multiple _start directives found"
                        )
                    start_address = instruction_offset
                    continue

                cmd = parts[0]
                opcode, has_arg = commands[cmd]

                if has_arg:
                    if len(parts) < 2:
                        raise ValueError(
                            f"Line {line_number}: Command '{cmd}' requires an argument"
                        )
                    if len(parts) > 2:
                        raise ValueError(
                            f"Line {line_number}: Too many arguments for command '{cmd}'"
                        )
                    try:
                        value = int(parts[1], 0)
                        value &= 0xFFFFFFFF
                    except ValueError:
                        raise ValueError(
                            f"Line {line_number}: Invalid argument for command '{cmd}': {parts[1]}"
                        )
                    instructions.append((opcode, value))
                    instruction_offset += 1
                else:
                    instructions.append((opcode, None))
                    instruction_offset += 1

            else:
                raise ValueError(
                    f"Line {line_number}: No section defined (.data, .text, or .proc)"
                )

    with open(instruction_mem_path, "wb") as f:
        f.write(struct.pack("I", start_address))
        for opcode, value in instructions:  # type: ignore
            f.write(struct.pack("B", opcode))
            if value is not None:
                f.write(struct.pack("<I", value))

    if data_entries:
        with open(data_mem_path, "wb") as f:
            max_addr = 0
            for addr, data_type, values in data_entries:
                if data_type == "word":
                    max_addr = max(max_addr, addr + len(values) * 4)
                elif data_type == "byte":
                    max_addr = max(max_addr, addr + len(values))
            if max_addr > memory_size:
                raise ValueError("Data memory size exceeds")
            data_memory = bytearray(memory_size)
            for addr, data_type, values in data_entries:
                if addr < 0 or addr + (4 if data_type == "word" else len(values)) > len(
                    data_memory
                ):
                    raise ValueError(f"Invalid data memory address: {addr}")
                if data_type == "word":
                    for i, value in enumerate(values):
                        struct.pack_into("<I", data_memory, addr + i * 4, value)
                else:
                    for i, value in enumerate(values):
                        data_memory[addr + i] = value

            f.write(data_memory)

