import sys
from typing import Optional

import os


def resource_path(relative_path: str) -> str:
    base_path: Optional[str]
    if hasattr(sys, "_MEIPASS"):
        base_path = getattr(sys, "_MEIPASS")
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
