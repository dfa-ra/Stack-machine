from .cpu import Cpu
from .cpu.mem import InstructionMem
from .inst_compiler.compiler import convert_to_binary


def compile_code(input_file: str, memory_size) -> int | None | bool:
    try:
        start_code = convert_to_binary(input_file, memory_size)
        return start_code
    except Exception as e:
        return False


def init_cpu(ep: int, mem) -> Cpu:
    i_mem = InstructionMem()
    return Cpu(8, mem, i_mem, ep)

