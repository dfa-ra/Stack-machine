from dataclasses import dataclass
from typing import Dict, Callable, List

from src.code_compiler.assembly.app.asm_info import get_mnemonic_by_opcode
from src.stack_machine.cpu.mem import DataMem, InstructionMem
from src.stack_machine.cpu.stack import Stack
from src.stack_machine.cpu.units import ControlAluUnit, ControlUnit, MemUnit



@dataclass
class SignalHandler:
    name: str
    action: Callable[["Cpu", int], None]


class Cpu:
    def __init__(self, stack_size: int, mem: DataMem, i_mem: InstructionMem, ep: int):
        self.data_stack: Stack = Stack(stack_size)
        self.ret_stack: Stack = Stack(stack_size)
        self.vector_stack: Stack = Stack(stack_size)
        self.mem: DataMem = mem
        self.i_mem: InstructionMem = i_mem
        self.regs = [0 for _ in range(4)]
        self.reg_names = {"A": 0, "B": 1, "PC": 2, "I": 3}
        self.set_reg("PC", ep)
        self.control_alu: ControlAluUnit = ControlAluUnit(self)  # type: ignore
        self.mem_unit: MemUnit = MemUnit(self)  # type: ignore
        self.control_unit: ControlUnit = ControlUnit(self)  # type: ignore
        self.last_alu_output = 0
        self.tick_count = 0
        self.running = True
        self.delay = 0
        self.simd_type = 0
        self.stop_flag = False

        # Определяем обработчики сигналов
        self.load_signals_handlers: Dict[str, SignalHandler] = {
            "load_imm": SignalHandler(
                "load_imm", lambda cpu, imm: cpu.set_reg("B", imm)
            ),
            "load_T_a": SignalHandler(
                "load_T_a", lambda cpu, _: cpu.set_reg("A", cpu.data_stack.get_T())
            ),
            "load_T_b": SignalHandler(
                "load_T_b", lambda cpu, _: cpu.set_reg("B", cpu.data_stack.get_T())
            ),
            "load_PC": SignalHandler(
                "load_PC", lambda cpu, _: cpu.set_reg("A", cpu.get_reg("PC"))
            ),
        }

        self.fetch_signals_handlers: Dict[str, SignalHandler] = {
            "fetch_pc": SignalHandler(
                "fetch_pc", lambda cpu, _: cpu.set_reg("PC", cpu.last_alu_output)
            ),
            "push_stack": SignalHandler("push_stack", lambda cpu, _: push_stack(cpu)),
            "pop_stack": SignalHandler("pop_stack", lambda cpu, _: pop_stack(cpu)),
            "call": SignalHandler("call", lambda cpu, _: call(cpu)),
            "restore_pc": SignalHandler("restore_pc", lambda cpu, _: restore_pc(cpu)),
            "over": SignalHandler("over", lambda cpu, _: over_stack(cpu)),
            "kill_cpu": SignalHandler(
                "kill_cpu", lambda cpu, _: setattr(cpu, "running", False)
            ),
        }

    def tick(  # type: ignore
        self, tick_logs: Callable[[Dict[str, List[str]]], None], command_log
    ) -> None:
        pc = self.get_reg("PC")
        if pc < 0 or pc >= len(self.i_mem.inst) or not self.running:
            self.running = False
            return
        # Получаем immediate и микрокоманды из декодера
        imm, micro_commands, mc_addr = self.control_unit.handle()
        # Обрабатываем каждую микрокоманду как отдельный такт
        command_log((get_mnemonic_by_opcode(mc_addr), imm))
        for micro_command in micro_commands:
            self.tick_count += 1

            type_s = micro_command.get("type", [])
            alu_s = micro_command.get("alu", [])
            mem_s = micro_command.get("mem", [])
            cpu_s = micro_command.get("cpu", [])

            self.simd_type = 0
            if type_s != []:
                if "simd" in type_s:
                    self.simd_type = 1

            if cpu_s != [] and len(cpu_s) > 0:
                for signal_name in cpu_s:
                    if signal_name in self.load_signals_handlers.keys():
                        handler = self.load_signals_handlers[signal_name]
                        handler.action(self, imm)  # type: ignore

            if alu_s != [] and len(alu_s) > 0:
                self.last_alu_output = self.control_alu.handle(alu_s)  # type: ignore

            if mem_s != [] and len(mem_s) > 0:
                self.mem_unit.handle(mem_s)

            if cpu_s != [] and len(cpu_s) > 0:
                for signal_name in cpu_s:
                    if signal_name in self.fetch_signals_handlers.keys():
                        handler = self.fetch_signals_handlers[signal_name]
                        handler.action(self, imm)  # type: ignore
            tick_logs(micro_command)

        self.set_reg("PC", self.get_reg("PC") + 1)

    def _print_state(self) -> str:
        cpu_condition = f"""  tick {self.tick_count}
  A  {self.regs[0]}
  B  {self.regs[1]}
  PC {self.regs[2]}
  I  {self.regs[3]}
  ALU {self.last_alu_output}
  data_stack {self.data_stack.stack}
  vector_stack {self.vector_stack.stack}"""
        return cpu_condition

    def get_reg(self, reg: int | str) -> int:
        if isinstance(reg, str):
            reg = self.reg_names[reg]
        return self.regs[reg]

    def set_reg(self, reg: int | str, val: int) -> None:
        if isinstance(reg, str):
            reg = self.reg_names[reg]
        self.regs[reg] = val


def push_stack(cpu: Cpu) -> None:
    if cpu.simd_type == 1:
        cpu.vector_stack.push(cpu.last_alu_output)
    else:
        cpu.data_stack.push(cpu.last_alu_output)


def pop_stack(cpu: Cpu) -> None:
    if cpu.simd_type == 1:
        cpu.vector_stack.pop()
    else:
        cpu.data_stack.pop()


def over_stack(cpu: Cpu) -> None:
    if cpu.simd_type == 1:
        cpu.vector_stack.over()
    else:
        cpu.data_stack.over()


def call(cpu: Cpu) -> None:
    cpu.ret_stack.push(cpu.get_reg("PC"))
    cpu.set_reg("PC", cpu.last_alu_output)


def restore_pc(cpu: Cpu) -> None:
    (cpu.set_reg("PC", cpu.ret_stack.get_T()),)  # type: ignore
    cpu.ret_stack.pop()
