from .cpu import Cpu
from .cpu.mem import InstructionMem, DataMem


def init_cpu(mem: DataMem, instr_path: str) -> Cpu:
    i_mem: InstructionMem = InstructionMem(instr_path)
    return Cpu(13, mem, i_mem, i_mem.start_pos)
