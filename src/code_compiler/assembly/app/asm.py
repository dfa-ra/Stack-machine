import struct
from typing import Tuple, List, Dict

import yaml  # type: ignore

from src.code_compiler.config import instruction_file


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
    exec_file = build_dir + "/exec.bin"

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

    write_combined_memory(
        exec_file, start_address, instructions, data_entries, memory_size
    )


def write_combined_memory(
    output_path: str,
    start_address: int,
    instructions: List[Tuple[str, int | None]],
    data_entries: List[Tuple[int, str, List[int]]],
    memory_size: int,
) -> None:
    with open(output_path, "wb") as f:
        f.write(struct.pack("<I", len(data_entries)))  # 32 бита - количество кластеров

        for addr, data_type, values in data_entries:
            if data_type == "word":
                cluster_size = len(values) * 4
                packed_values = b"".join(struct.pack("<I", v) for v in values)
            else:
                cluster_size = len(values)
                packed_values = bytes(values)

            # Проверяем, что кластер помещается в память
            if addr < 0 or addr + cluster_size > memory_size:
                raise ValueError(f"Invalid data memory address: {addr}")

            f.write(struct.pack("<I", cluster_size))
            f.write(struct.pack("<I", addr))

            # Записываем данные кластера
            f.write(packed_values)

        # 3. Записываем инструкции
        f.write(struct.pack("<I", start_address))  # Стартовый адрес
        for opcode, value in instructions:
            f.write(struct.pack("B", opcode))
            if value is not None:
                f.write(struct.pack("<I", value))
