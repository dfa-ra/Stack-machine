from typing import List

from ..compile_conf import commands
from .compiler_text import CompilerText


class CompilerFunc:
    def __init__(self, compiler) -> None:  # type: ignore
        self.compiler = compiler
        self.output_func: List[str] = []
        self.compiler_text: CompilerText = CompilerText(self.compiler)
        pass

    def emit_func(self, command: str, operand: int = None) -> None:  # type: ignore
        if command in commands:
            self.output_func.append(
                f"{command} {operand}" if commands[command] else command
            )
            self.compiler.pc += 1

    def compile(
        self, lines: List[str], address_space: int, intermediate_var: int
    ) -> int:
        func: List[str] = []
        end_func_flag = False
        for line in lines:
            if line.startswith(":"):
                if end_func_flag:
                    raise Exception("Previous function not finished")
                end_func_flag = True
                func_name = line[2:-1] + line[-1]
                self.compiler.functions[func_name] = self.compiler.pc
                continue

            line = line.strip()
            if line == ";":
                if not end_func_flag:
                    raise Exception("Function not started")
                end_func_flag = False
                intermediate_var = self.compiler_text.compile(
                    func, address_space, intermediate_var
                )
                self.output_func += self.compiler_text.output_text
                self.emit_func("ret")
                self.compiler_text.output_text = []
                func = []
                continue

            func.append(line)
        if end_func_flag:
            raise Exception("The function is not finished")
        return intermediate_var
