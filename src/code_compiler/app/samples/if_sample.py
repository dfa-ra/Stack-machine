def get_if_sample(token):
    result = []
    if token == "<":  # a < b | b - a + 1 > 0
        result = [
            "-",
            "push_imm -1",
            "+",
            "-if 2",
            "push_imm 0",
            "jmp 1",
            "push_imm 1"
        ]
    elif token == "<=":  # a < b
        result = [
            "-",
            "-if 2",
            "push_imm 0",
            "jmp 1",
            "push_imm 1"
        ]
    elif token == ">":  # a < b
        result = [
            "-",
            "not",
            "inc",
            "push_imm -1",
            "+",
            "-if 2",
            "push_imm 0",
            "jmp 1",
            "push_imm 1"
        ]
    elif token == ">=":  # a < b
        result = [
            "-",
            "not",
            "inc",
            "-if 2",
            "push_imm 0",
            "jmp 1",
            "push_imm 1"
        ]
    elif token == "=":  # a = b | a - b = 0
        result = [
            "-",
            "if 2",
            "push_imm 0",
            "jmp 1",
            "push_imm 1"
        ]
    elif token == "!=":  # T != 0
        result = [
            "-",
            "if 2",
            "push_imm 1",
            "jmp 1",
            "push_imm 0"
        ]


    return result
