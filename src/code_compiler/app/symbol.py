from typing import List


class Symbol:
    def __init__(self, address: int, type: str, size: int = 1, values: List = []):  # type: ignore
        self.address = address
        self.type = type
        self.size = size
        self.values = values if values else []
