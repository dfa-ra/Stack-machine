from typing import List


class Scope:
    def __init__(self) -> None:
        self.scopes: List[List[str]] = [[]]

    def pop(self) -> None:
        self.scopes.pop()

    def get_scope(self) -> List[str]:
        scope = self.scopes[-1]
        self.scopes.pop()
        return scope

    def add_scope(self, scope: List[str]) -> None:
        self.scopes.append(scope)

    def add_text(self, token: str) -> None:
        self.scopes[-1].append(token)
