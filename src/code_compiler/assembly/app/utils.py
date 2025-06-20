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
