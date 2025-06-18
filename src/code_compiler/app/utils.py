def is_hex_string(s: str) -> bool:
    if not s.startswith('0x'):
        return False
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def hex_to_int(s: str) -> int:
    if is_hex_string(s):
        return int(s, 16)
    raise ValueError(f"Строка '{s}' не является валидным шестнадцатеричным числом")