from typing import List

from .if_sample import get_if_sample


class LoopSample:
    def __init__(self) -> None:
        self.condition = 0
        self.body_len = 0
        self.steps_to_check_data: List[str] = []
        self.increase_counter: List[str] = []
        self.compare_token = ""
        self.counter_address = 0

    def init_increase_counter(self) -> None:
        self.increase_counter = [
            "dup",
            f"lw_from_imm_addr {self.counter_address}",
            "+",
            f"sw_to_imm_addr {self.counter_address}",
            f"jmp -{self.body_len + 4 + len(self.steps_to_check_data) + 1}",
            "pop",
            "pop",
        ]

    def init_steps_to_check_data(self) -> None:
        self.steps_to_check_data = (
            [
                "over",
                "dup",
                f"lw_from_imm_addr {self.counter_address}",
                "over",
            ]
            + get_if_sample(self.compare_token)
            + [
                f"if {self.body_len + 1 + 5}",
                "over",
            ]
        )
