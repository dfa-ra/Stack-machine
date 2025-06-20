import argparse
import os

from src.code_compiler.assembly.app.asm import convert_to_binary


def assembly(build: str, file: str, mem_size: int) -> int:
    return convert_to_binary(build, file, mem_size)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Парсер для конфига и .forth файла")
    parser.add_argument("code_file", type=str, help="Путь к файлу .forth")
    parser.add_argument("mem_size", type=int, help="Размер памяти данных")
    args = parser.parse_args()
    wd = os.path.dirname(os.path.abspath(__file__)) + "/"
    if args.code_file.startswith("/"):
        wd = ""
    file_path = wd + args.code_file
    build_dir = os.path.join(os.path.dirname(file_path))
    print(assembly(build_dir, file_path, args.mem_size))
