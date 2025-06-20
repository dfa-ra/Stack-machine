import re
from typing import Callable, Any, Dict, List, Tuple

from src.stack_machine.cpu import Cpu
from src.stack_machine.utils.bitwise_utils import btle, tsfb
from src.code_compiler.assembly.app.asm_info import get_decompiled_code


def ascii_to_string(num: int) -> str:
    return "".join(chr(num))


class logger:
    def __init__(self, cpu_: Cpu, log_fmt, instruction_mem_path: str):  # type: ignore
        """

        :rtype: object
        """
        self.instruction_mem_path = instruction_mem_path
        self.cpu_: Cpu = cpu_
        self.fmt = log_fmt
        self.micro_command: Dict[str, List[str]] = {}
        self.token_map: Dict[str, Callable] = {  # type: ignore
            "cpu": self.resolve_register_tokens,
            "stack": self.resolve_stack_tokens,
            "io": self.resolve_io_tokens,
            "condition": self.resolve_condition_token,
            "instruction": self.resolve_instruction_mem,
            "microcode": self.resolve_microcode,
            "command": self.resolve_command,
        }
        self.stack_resolve_list: Dict[str, Callable[Any]] = {  # type: ignore
            "data": lambda: self.cpu_.data_stack.stack,
            "vector": lambda: self.cpu_.vector_stack.stack,
            "return": lambda: self.cpu_.ret_stack.stack,
        }
        self.reg_resolve_list: Dict[str, Callable[Any]] = {  # type: ignore
            "A": lambda: self.cpu_.get_reg("A"),
            "B": lambda: self.cpu_.get_reg("B"),
            "T": lambda: self.cpu_.data_stack.get_T(),
            "V_T": lambda: self.cpu_.vector_stack.get_T(),
            "tick": lambda: self.cpu_.tick_count,
        }
        self.io_resolve_map: Dict[str, Callable[Any]] = {  # type: ignore
            "in": lambda: self.cpu_.mem.get_in(),
            "out": lambda: self.cpu_.mem.get_out(),
        }
        self.integer_convertion: Dict[str, Callable[Any]] = {  # type: ignore
            "hex": (lambda x: ", ".join([hex(_i) for _i in x])),
            "bin": (lambda x: ", ".join([bin(_i) for _i in x])),
            "dec": (lambda x: ", ".join([str(tsfb(_i)) for _i in x])),
            "decbe": (lambda x: ", ".join([str(tsfb(btle(_i))) for _i in x])),
            "str": (lambda x: "".join([ascii_to_string(_i) for _i in x])),
        }

    def resolve_instruction_mem(self, token_list: list[str]) -> str:
        return get_decompiled_code(self.instruction_mem_path)

    def resolve_command(
        self, token_list: list[str]
    ) -> Callable[[tuple[str, int]], None]:
        return self.command

    def resolve_microcode(self, token_list: list[str]) -> str:
        lines = []
        for key, values in self.micro_command.items():
            line = f"{key}: {', '.join(values)}"
            lines.append(line)
        return " | ".join(lines)

    def resolve_stack_tokens(self, token_list: list[str]) -> List[str] | str:
        if token_list[0] not in self.stack_resolve_list:
            raise ValueError(f"got unknown stack: {token_list[0]}")
        if len(token_list) == 1:
            return str(self.stack_resolve_list[token_list[0]]())
        if token_list[1] not in self.integer_convertion:
            raise ValueError(f"got unknown integer format: {token_list[1]}")
        return [
            self.integer_convertion[token_list[1]]([num])
            for num in self.stack_resolve_list[token_list[0]]()
        ]

    def resolve_register_tokens(self, token_list: list[str]) -> str:
        if token_list[0] not in self.reg_resolve_list:
            raise ValueError(f"got unknown register: {token_list[0]}")
        if len(token_list) == 1:
            return str(self.reg_resolve_list[token_list[0]]())
        if token_list[1] not in self.integer_convertion:
            raise ValueError(f"got unknown integer format: {token_list[1]}")
        return self.integer_convertion[token_list[1]](  # type: ignore
            [self.reg_resolve_list[token_list[0]]()]
        )

    def resolve_io_tokens(self, token_list: list[str]) -> str:
        if token_list[0] not in self.io_resolve_map:
            raise ValueError(f"got unknown io: {token_list[0]}")
        if token_list[1] not in self.integer_convertion:
            raise ValueError(f"got unknown integer format: {token_list[1]}")
        return self.integer_convertion[token_list[1]](  # type: ignore
            self.io_resolve_map[token_list[0]]()
        )

    def resolve_condition_token(self, tokens: str) -> str:
        actual_tokens = ":".join(tokens)
        condition_left = actual_tokens[
            actual_tokens.find("[") + 1 : actual_tokens.find("]")
        ]
        init_cond_left = condition_left
        condition_left = condition_left.split(":")  # type: ignore
        condition_right = actual_tokens[
            actual_tokens.rfind("[") + 1 : actual_tokens.rfind("]")
        ]
        if condition_left[0] in self.token_map:
            condition_left = self.token_map[condition_left[0]](condition_left[1:])
        else:
            raise ValueError(f"bad token was given in assertion: {condition_left}")
        result = "Failed"
        if condition_left == condition_right:
            result = "Passed"
        return f"[{condition_left}]({init_cond_left})=[{condition_right}] => RESULT={result}"

    def resolve_log_token(self, tokens) -> str:  # type: ignore
        token_list = tokens.split(":")
        if token_list[0] in self.token_map:
            return self.token_map[token_list[0]](token_list[1:])  # type: ignore
        else:
            raise ValueError(f"bad token was given: {tokens}")

    def run_log(self, condition: str) -> None:
        for i in self.fmt:
            if i["slice"] == condition:
                print(
                    i["name"]
                    + ": "
                    + re.sub(
                        r"\{([^{}]+)\}",
                        lambda m: self.resolve_log_token(m.group(1)),
                        i["view"],
                    ).replace("\n", "\n")[:-1]
                )

    def each_tick_logs(self, micro_command: Dict[str, List[str]]) -> None:
        self.micro_command = micro_command
        self.run_log("all")

    def command(self, command: Tuple[str, int]) -> None:
        if command[1] is None:
            print(f"Command: {command[0]}")
        else:
            print(f"Command: {command[0]} {int(command[1])}")

    def run_assert(self) -> None:
        print("-----------")
        self.run_log("last")
        print("-----------")

    def run_binary(self) -> None:
        print("-----------")
        self.run_log("mem")
        print("-----------")
