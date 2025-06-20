import os
from typing import List, Dict

from src.code_compiler.compiling.app.compilers import (
    CompilerText,
    CompilerData,
    CompilerFunc,
)
from src.code_compiler.compiling.app.symbol import Symbol


class Compiler:
    def __init__(self, file_path: str) -> None:
        self.symbols: List[List[Symbol]] = []
        self.file_path = file_path
        self.address_space_count = 0
        self.data_address = 0
        self.functions: Dict[str, int] = {}
        self.output: List[str] = []
        self.pc = 0

        self.compiler_data: CompilerData = CompilerData(self)
        self.compiler_text: CompilerText = CompilerText(self)
        self.compiler_func: CompilerFunc = CompilerFunc(self)

    def compile_import(self, lines: List[str]) -> None:
        for line in lines:
            filename = line.strip('"')
            try:
                with open(
                    os.path.join(os.path.dirname(self.file_path), filename), "r"
                ) as f:
                    imported_code = f.read()
                    self.compile(imported_code)
            except FileNotFoundError:
                print(f"Ошибка: файл {filename} не найден")
        self.address_space_count += 1

    def compile_data(self, lines: List[str]) -> None:
        self.data_address = self.compiler_data.compile(lines, self.data_address)

    def compile_func(self, lines: List[str], address_space: int) -> None:
        self.data_address = self.compiler_func.compile(
            lines, address_space, self.data_address
        )

    def compile_text(self, lines: List[str], address_space: int) -> None:
        self.data_address = self.compiler_text.compile(
            lines, address_space, self.data_address
        )

    def compile(self, code: str) -> None:
        lines = code.strip().split("\n")
        current_section = None
        import_lines = []
        data_lines = []
        func_lines = []
        text_lines = []

        for line in lines:
            line = line.split("#")[0]
            line = line.strip()
            if not line:
                continue
            if line in ["_data_", "_func_", "_text_", "_import_"]:
                current_section = line
                continue
            if current_section == "_import_":
                import_lines.append(line)
            elif current_section == "_data_":
                data_lines.append(line)
            elif current_section == "_func_":
                func_lines.append(line)
            elif current_section == "_text_":
                text_lines.append(line)

        if import_lines:
            self.compile_import(import_lines)
        if data_lines:
            self.compile_data(data_lines)
        if func_lines:
            self.compile_func(func_lines, self.address_space_count)
        if text_lines:
            self.compile_text(text_lines, self.address_space_count)

    def get_text_section(self) -> List[str]:
        return (
            ["   .text"]
            + self.compiler_func.output_func
            + ["   _start"]
            + self.compiler_text.output_text
        )

    def get_compiled_code(self) -> str:
        text = "\n".join(self.compiler_data.get_data_section())
        text += "\n"
        text += "\n".join(self.get_text_section())
        return text
