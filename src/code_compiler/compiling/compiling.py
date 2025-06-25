import argparse
import os

from src.code_compiler.compiling.app import Compiler
from src.common import resource_path


def compile_code(file_path: str, build: str) -> None:
    with open(os.path.join(file_path)) as code_file:
        code = code_file.read()

    if not os.path.exists(build):
        os.makedirs(build)

    compiler = Compiler(file_path)
    try:
        compiler.compile(code)
    except Exception as e:
        print(str(e))
    result = compiler.get_compiled_code()

    with open(os.path.join(build, "code"), "w") as mnemonic_code_file:
        mnemonic_code_file.write(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Парсер для конфига и .forth файла")
    parser.add_argument("forth_file", type=str, help="Путь к файлу .forth")
    args = parser.parse_args()
    file_path = resource_path(args.forth_file)
    build_dir = os.path.join(os.path.dirname(file_path), "build")
    compile_code(file_path, build_dir)
