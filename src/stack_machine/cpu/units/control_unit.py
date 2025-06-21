from typing import Tuple

from src.stack_machine.cpu.instruction import Instruction
from src.stack_machine.cpu.micro_command import MicroCommand

# в тупую интерпритирует сигналы


# смотри на аддрес мк (в самой инструкции) и набивает список сигналов
class ControlUnit:
    def __init__(self, cpu):  # type: ignore
        self.cpu = cpu
        self.mc_rom = MicroCommand()

    def handle(self) -> Tuple[int | None, list[dict[str, list[str]]], int]:
        inst_addr = self.cpu.get_reg("PC")

        inst_ = Instruction(self.cpu.i_mem.get_inst(inst_addr))

        imm: int | None = inst_.imm
        mc_addr: int = inst_.mc_addr

        micro_commands = self.mc_rom.decode_microcode(mc_addr)

        return imm, micro_commands, mc_addr
