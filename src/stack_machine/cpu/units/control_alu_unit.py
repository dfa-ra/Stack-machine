import multiprocessing
from typing import List, Tuple

from src.stack_machine.cpu.units.alu_unit import ALU
from src.stack_machine.cpu.units.vector_unit import VectorUnit


def run_search(obj: ALU, signals, a: int, b: int, index: int, result_queue) -> None:  # type: ignore
    result = obj.handle(signals, a, b)
    result_queue.put((index, result))


class ControlAluUnit:
    def __init__(self, cpu):  # type: ignore

        self.cpu = cpu
        self.alu1: ALU = ALU(cpu)
        self.alu2: ALU = ALU(cpu)
        self.alu3: ALU = ALU(cpu)
        self.alu4: ALU = ALU(cpu)

    def init_alu_list(self) -> List[ALU]:
        return [self.alu1, self.alu2, self.alu3, self.alu4]

    def init_operands(self, signals: List[str]) -> List[int] | List[Tuple[int, int]]:
        if self.cpu.simd_type == 1:
            left: List[int] = [0, 0, 0, 0]
            right: List[int] = [0, 0, 0, 0]
            if "open_l" in signals:
                left = VectorUnit.slice(self.cpu.vector_stack.pop())
            if "open_r" in signals:
                right = VectorUnit.slice(self.cpu.vector_stack.pop())
            return [(left[i], right[i]) for i in range(0, len(left))]
        else:
            left_int = 0
            right_int = 0
            if "open_a" in signals:
                left_int = self.cpu.get_reg("A")
            if "open_b" in signals:
                right_int = self.cpu.get_reg("B")
            if "open_r_pc" in signals:
                left_int = self.cpu.get_reg("PC")
            if "open_l" in signals:
                left_int = self.cpu.data_stack.pop()
            if "open_r" in signals:
                right_int = self.cpu.data_stack.pop()
            return [left_int, right_int]

    def handle(self, signals: List[str]) -> List[int] | int:
        if self.cpu.simd_type == 1:
            return self.simd_handle(signals)
        else:
            return self.scalar_handle(signals)

    def scalar_handle(self, signals: List[str]) -> int:
        operands = self.init_operands(signals)
        return self.alu1.handle(signals, operands[0], operands[1])  # type: ignore

    def simd_handle(self, signals: List[str]) -> List[int]:
        results = multiprocessing.Queue()  # type: ignore
        processes = []
        alu_list = self.init_alu_list()
        operands = self.init_operands(signals)

        for i, (obj, (a, b)) in enumerate(zip(alu_list, operands)):  # type: ignore
            p = multiprocessing.Process(
                target=run_search,
                args=(obj, signals, a, b, i, results),  # type: ignore
                name=f"Alu-{i + 1}"
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        process_results: List[int] = [0] * len(operands)
        while not results.empty():
            index, result = results.get()
            process_results[index] = result

        return process_results
