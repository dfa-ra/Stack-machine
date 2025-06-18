from ..instruction import Instruction
from ..micro_command import MicroCommand
from ..signals import CommonSignal


# в тупую интерпритирует сигналы


# смотри на аддрес мк (в самой инструкции) и набивает список сигналов
class ControlUnit:

    def __init__(self, cpu):
        self.cpu = cpu

    def handle(self) -> [int, list[list[CommonSignal]]]:
        inst_addr = self.cpu.get_reg("PC")

        inst_ = Instruction(self.cpu.i_mem.get_inst(inst_addr))

        imm = inst_.imm
        mc_addr = inst_.mc_addr

        micro_commands = MicroCommand.decode_microcode(mc_addr)

        return imm, micro_commands
