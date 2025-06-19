from typing import List


class VectorUnit:
    @staticmethod
    def slice(vec: List[int]) -> List[int]:
        return [vec[0], vec[1], vec[2], vec[3]]

    @staticmethod
    def compound(a: int, b: int, c: int, d: int) -> List[int]:
        return [a, b, c, d]
