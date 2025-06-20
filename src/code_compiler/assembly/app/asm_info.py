import struct

import yaml  # type: ignore

from src.code_compiler.assembly.app.utils import ltbe
from src.code_compiler.config.config import instruction_file


def get_mnemonic_by_opcode(opcode: int):  # type: ignore
    with open(instruction_file, "r") as f:
        commands = yaml.safe_load(f)["commands"]
    opcode_to_mnemonic = {cmd["opcode"]: cmd["desc"] for cmd in commands}
    return opcode_to_mnemonic.get(opcode, f"UNKNOWN_{hex(opcode)}")


def get_decompiled_code_debug(instruction_mem_path: str, num_line: int = 0) -> str:
    with open(instruction_file, "r") as f:
        data = yaml.safe_load(f)["commands"]
        opcode_to_mnemonic = {cmd["opcode"]: cmd["desc"] for cmd in data}
        opcode_has_arg = {cmd["opcode"]: cmd.get("operand", False) for cmd in data}

    with open(instruction_mem_path, "rb") as f:
        byte_data = f.read()

    result = []
    count = 0
    index = 0

    while index < len(byte_data):
        opcode = byte_data[index]
        index += 1

        mnemonic = opcode_to_mnemonic.get(opcode, f"UNKNOWN_{hex(opcode)}")
        has_arg = opcode_has_arg.get(opcode, False)

        if has_arg:
            if index + 4 > len(byte_data):
                result.append(
                    f"  ERROR: Incomplete argument for {mnemonic} at byte {index - 1}"
                )
                break
            value = struct.unpack_from("<I", byte_data, index)[0]
            index += 4
            if count == num_line:
                result.append(f"  {mnemonic} 0x{value:08X}  <--")
            else:
                result.append(f"  {mnemonic} 0x{value:08X}")
        else:
            if count == num_line:
                result.append(f"  {mnemonic}  <--")
            else:
                result.append(f"  {mnemonic}")
        count += 1

    return "\n".join(result)


def get_decompiled_code(instruction_mem: bytearray) -> str:
    with open(instruction_file, "r") as f:
        data = yaml.safe_load(f)["commands"]
        opcode_to_mnemonic = {cmd["opcode"]: cmd["desc"] for cmd in data}
        opcode_has_arg = {cmd["opcode"]: cmd.get("operand", False) for cmd in data}

    result = []
    count = 0
    index = 4

    while index < len(instruction_mem):
        opcode = instruction_mem[index]
        index += 1

        mnemonic = opcode_to_mnemonic.get(opcode, f"UNKNOWN_{hex(opcode)}")
        has_arg = opcode_has_arg.get(opcode, False)

        if has_arg:
            if index + 4 > len(instruction_mem):
                result.append(
                    f"  ERROR: Incomplete argument for {mnemonic} at byte {index - 1}"
                )
                break
            value = struct.unpack_from("<I", instruction_mem, index)[0]
            command = ((opcode & 0xFF) << 32) | (ltbe(value) & 0xFFFFFFFF)
            result.append(
                f"0x{(index - 1):03x} - 0x{command:010x} - {mnemonic} 0x{value:08X}"
            )
            index += 4
        else:
            command = opcode & 0xFF
            result.append(f"0x{(index - 1):03x} - 0x{command:02x} - {mnemonic}")
        count += 1

    return "\n".join(result)


def get_data_meminfo(instruction_mem_path: str, start: int = 0, end: int = 0) -> str:
    mem_info: str = ""
    with open(instruction_mem_path, "rb") as f:
        byte_data = f.read()
        if end == 0:
            end = len(byte_data)
        # Вывод таблицы
        mem_info += "  Addr |  0  1  2  3 |  4  5  6  7 |  8  9 10 11 |\n"
        mem_info += "  -----|-------------|-------------|-------------|\n"

        for i in range(start, end, 12):
            # Адрес в шестнадцатеричном формате
            addr = i
            # Получаем до 12 байт для текущей строки
            chunk = byte_data[i : i + 12]
            # Форматируем байты в строку, разбивая на чанки по 4 байта
            bytes_str = []
            for j in range(12):
                if j < len(chunk):
                    bytes_str.append(f"{chunk[j]:02X}")
                else:
                    bytes_str.append("  ")  # Пробелы для недостающих байт
            # Разделяем на три чанка по 4 байта
            group1 = " ".join(bytes_str[0:4])
            group2 = " ".join(bytes_str[4:8])
            group3 = " ".join(bytes_str[8:12])
            # Выводим строку
            mem_info += (
                f"  {addr:04X} | {group1: <10} | {group2: <10} | {group3: <10} |"
            )
            mem_info += "\n"
    return mem_info
