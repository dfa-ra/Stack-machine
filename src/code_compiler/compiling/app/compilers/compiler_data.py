from typing import Dict, List

from src.code_compiler.compiling.app.symbol import Symbol
from src.code_compiler.compiling.app.compile_conf import forbidden_var
from src.code_compiler.compiling.app.utils import is_hex_string, hex_to_int


class CompilerData:
    def __init__(self, compiler) -> None:  # type: ignore
        self.compiler = compiler
        self.data_address = 0
        self.symbols: Dict[str, Symbol] = {}

    def add_data(self, name: str, type: str, size: int = 1, values: List = []) -> None:  # type: ignore
        self.symbols[name] = Symbol(self.data_address, type, size, values)
        if type == "str":
            self.data_address += size
        else:
            self.data_address += size * 4

    def compile(self, lines: List[str], data_address: int) -> int:
        self.data_address = data_address
        for line in lines:
            tokens = line.split()
            if tokens[-1] in forbidden_var:
                raise Exception("Forbidden variable")
            if tokens[0].startswith("["):
                name = tokens[-1]
                values: List[str] = []
                for value in tokens[1:]:
                    if value == "]":
                        break
                    values.append(value)
                self.add_data(name, "array", int(tokens[-3]), values)
            elif tokens[0].startswith('"'):
                start = line.find('"') + 1
                end = line.find('"', start)
                result = line[start:end]
                size = len(result)
                if tokens[-2].isdigit():
                    size = max(size, int(tokens[-2]))
                self.add_data(tokens[-1], "str", size + 1, [result])
            elif tokens[1] == "VAR":
                if is_hex_string(tokens[0]):
                    self.add_data(tokens[2], "var", 1, [hex_to_int(tokens[0])])
                else:
                    self.add_data(tokens[2], "var", 1, [int(tokens[0])])
        self.compiler.symbols.append(self.symbols.copy())
        self.symbols.clear()
        return self.data_address

    def get_symbol(self, name: str) -> Symbol:
        return self.compiler.symbols[name]  # type: ignore

    def get_data_section(self) -> List[str]:
        data = ["   .data"]
        for space in self.compiler.symbols:
            for name, symbol in space.items():
                if symbol.type == "array":
                    data.append(
                        f"var {symbol.address} word {' '.join(map(str, symbol.values))}"
                    )
                elif symbol.type == "str":
                    data.append(
                        f"var {symbol.address} byte {' '.join(map(str, str_parse(symbol.values[0])))}"
                    )
                else:
                    data.append(f"var {symbol.address} word {symbol.values[0]}")
        return data


def str_parse(token: str) -> List[int]:
    ascii_result = [ord(c) for c in token]
    ascii_result.append(0)
    return ascii_result
