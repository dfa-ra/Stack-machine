from .cpu import Cpu
from .cpu.mem import InstructionMem, DataMem
from src.stack_machine.inst_compiler.compiler import convert_to_binary


def compile_code(input_file: str, memory_size: int) -> int:
    start_code: int = convert_to_binary(input_file, memory_size)
    return start_code


def init_cpu(ep: int, mem: DataMem, instr_path: str) -> Cpu:
    i_mem: InstructionMem = InstructionMem(instr_path)
    return Cpu(13, mem, i_mem, ep)
