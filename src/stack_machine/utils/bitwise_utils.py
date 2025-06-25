def btle(value: int) -> int:
    value = value & 0xFFFFFFFF
    if value < 0 or value > 0xFFFFFFFF:
        raise ValueError("Value must be a 32-bit integer (0 to 0xFFFFFFFF)")

    byte0 = (value >> 24) & 0xFF
    byte1 = (value >> 16) & 0xFF
    byte2 = (value >> 8) & 0xFF
    byte3 = value & 0xFF

    result = (byte3 << 24) | (byte2 << 16) | (byte1 << 8) | byte0
    return result


def ltbe(value: int) -> int:
    value = value & 0xFFFFFFFF
    if value < 0 or value > 0xFFFFFFFF:
        raise ValueError("Value must be a 32-bit integer (0 to 0xFFFFFFFF)")

    byte0 = value & 0xFF
    byte1 = (value >> 8) & 0xFF
    byte2 = (value >> 16) & 0xFF
    byte3 = (value >> 24) & 0xFF

    result = (byte0 << 24) | (byte1 << 16) | (byte2 << 8) | byte3
    return result


def tsfb(value: int) -> int:
    if value < 0 or value > 0xFFFFFFFF:
        raise ValueError("Value must be a 32-bit integer (0 to 0xFFFFFFFF)")

    bytes_value = value.to_bytes(4, byteorder="big")
    return int.from_bytes(bytes_value, byteorder="big", signed=True)
