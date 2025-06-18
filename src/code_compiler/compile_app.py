import os

from .app import Compiler


def compile_code(file_path: str, build: str):
    with open(os.path.join(file_path)) as code_file:
        code = code_file.read()

    if not os.path.exists(build):
        os.makedirs(build)

    compiler = Compiler()
    compiler.compile(code)
    result = compiler.get_compiled_code()

    with open(os.path.join(build, "code"), "w") as mnemonic_code_file:
        mnemonic_code_file.write(result)


if __name__ == '__main__':
    path = "examples/program.forth"
    wd = os.path.dirname(os.path.abspath(__file__))

    compile_code(wd + "/" + path, "/media/ra/_work/ra/ITMO/CSA/lab4/src/code_compiler/examples/")
