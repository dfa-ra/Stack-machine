from typing import List

from ..compile_conf import built_in_words, commands
from ..samples import LoopSample, get_if_sample
from ..scope import Scope
from ..symbol import Symbol
from ..utils import is_hex_string, hex_to_int


class CompilerText:
    def __init__(self, compiler):
        self.compiler = compiler
        self.intermediate_var = 0
        self.scope = Scope()
        self.output_text = []
        self.loop_flag = 0
        self.loop_sample: List[LoopSample] = []
        self.if_sample: List[LoopSample] = []
        self.compare_token = ""

    def emit(self, command, operand=None):
        if command in commands:
            self.scope.add_text(f"{command} {operand}" if commands[command] else command)
            self.compiler.pc += 1
        else:
            self.scope.add_text(f"; {command}")

    def compile(self, lines, address_space, intermediate_var):
        self.intermediate_var = intermediate_var
        self.scope.add_scope([])
        for line in lines:
            tokens = line.split()
            for token in tokens:
                if token == "LOOP":
                    self.loop_flag = 1
                    self.scope.add_scope([])
                    # self.emit("------- loop -------")
                    self.loop_sample.append(LoopSample())
                elif token == "WHILE":
                    self.loop_flag = 2
                    self.loop_sample[len(self.loop_sample) - 1].compare_token = self.compare_token
                    self.scope.add_scope([])
                elif token == "REPEAT":
                    self.loop_flag = 3
                    self.loop_sample[-1].body_len = len(self.scope.scopes[-1])
                    self.loop_sample[-1].init_steps_to_check_data()
                    self.loop_sample[-1].init_increase_counter()
                    self.scope.scopes[-2] += (
                            self.loop_sample[-1].steps_to_check_data +
                            # ["; ------- loop body start -------"] +
                            self.scope.scopes[-1] +
                            # ["; ------- loop body end -------"] +
                            self.loop_sample[-1].increase_counter
                    )

                    self.compiler.pc += len(self.loop_sample[-1].steps_to_check_data) + len(self.loop_sample[-1].increase_counter)
                    self.scope.scopes[-3] += self.scope.scopes[-2]
                    # self.emit("------- end loop -------")
                    self.loop_sample.pop()

                    self.scope.pop()
                    self.scope.pop()
                elif token == "IF":
                    self.scope.scopes[-1] += get_if_sample(self.compare_token)
                    self.compiler.pc += len(get_if_sample(self.compare_token))
                    self.scope.add_scope([])
                elif token == "ELSE":
                    self.scope.add_scope([])
                elif token == "THEN":
                    self.scope.scopes[-3] += (
                            [f"if {len(self.scope.scopes[-2]) + 1}"] +
                            self.scope.scopes[-2] +
                            [f"jmp {len(self.scope.scopes[-1])}"] +
                            self.scope.scopes[-1]
                    )
                    self.compiler.pc += 2
                    self.scope.pop()
                    self.scope.pop()
                elif token in ["<", "<=", ">", ">=", "=", "!="]:
                    self.compare_token = token
                else:
                    self.compile_text(token, address_space)
        self.output_text = self.scope.get_scope()
        return self.intermediate_var

    def compile_text(self, token, address_space):
        if len(self.compiler.symbols) > 0 and address_space < len(self.compiler.symbols) and token in \
                self.compiler.symbols[address_space]:
            if self.compiler.symbols[address_space][token].type == 'array':
                self.emit('v_lw_from_imm_addr', self.compiler.symbols[address_space][token].address)
            else:
                self.emit('lw_from_imm_addr', self.compiler.symbols[address_space][token].address)
        elif token in self.compiler.functions.keys():
            offset = self.compiler.functions[token] - self.compiler.pc - 1
            self.emit('call', offset)
        elif token == 'a!':
            self.emit('load_T_a_pop')
        elif token == 'a':
            self.emit('push_a')
        elif token == 'b!':
            self.emit('load_T_b_push')
        elif token == 'v!':
            self.emit('v_sw_to_a_addr')
        elif token == 'v@':
            self.emit('v_lw_from_a_addr')
        elif token.startswith('!'):
            if len(token) > 1:
                if token[1] == "+" and len(token) == 2:
                    self.emit('sw_to_a_addr_inc_a')
                elif token[1] == "b" and len(token) == 2:
                    self.emit('sw_to_b_addr')

                else:
                    name = token[1:]
                    if len(self.compiler.symbols) == 0 or name not in self.compiler.symbols[address_space].keys():
                        if len(self.compiler.symbols) == 0:
                            self.compiler.symbols.append({})
                        self.compiler.symbols[address_space][name] = Symbol(self.intermediate_var, 'var', 1, [0])
                        if self.loop_flag == 1:
                            self.loop_sample[len(self.loop_sample)-1].counter_address = self.intermediate_var
                        self.intermediate_var += 4
                        self.emit("sw_to_imm_addr", self.compiler.symbols[address_space][name].address)

                    elif self.compiler.symbols[address_space][name].type == 'array':
                        self.emit("load_T_a_pop")
                        self.emit('sw_to_a_addr')
                    else:
                        self.emit("sw_to_imm_addr", self.compiler.symbols[address_space][name].address)
            else:
                self.emit('sw_to_a_addr')
        elif token.startswith('@'):
            if len(token) > 1:
                if token[1] == "+" and len(token) == 2:
                    self.emit('lw_from_a_addr_inc_a')
                elif token[1] == "b" and len(token) == 2:
                    self.emit('lw_from_b_addr')
                else:
                    name = token[1:]
                    if self.compiler.symbols[address_space][name].type == 'array':
                        self.emit("load_T_a_pop")
                        self.emit('lw_from_a_addr')
                    else:
                        self.emit("lw_from_imm_addr", self.compiler.symbols[address_space][name].address)
            else:
                self.emit('lw_from_a_addr')
        elif token.startswith('&'):
            name = token[1:]
            self.emit('push_imm', self.compiler.symbols[address_space][name].address)
        elif token.isdigit() or (token.startswith("-") and token[1:].isdigit()):
            self.emit('push_imm', token)
        elif is_hex_string(token):
            self.emit('push_imm', hex_to_int(token))
        elif token in built_in_words:
            self.emit(built_in_words[token])
        else:
            raise Exception(f'Unknown token: {token}')

