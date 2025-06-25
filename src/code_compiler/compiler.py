import argparse
import os

import yaml  # type: ignore

from src.code_compiler.assembly.assembly import assembly
from src.code_compiler.compiling.compiling import compile_code
from src.common import resource_path


def main(file_path: str, build: str, conf_path: str) -> None:
    conf = yaml.safe_load(open(conf_path))
    compile_code(file_path, build)
    assembly(build, build + "/code", int(conf["memory_size"]))
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Парсер для конфига и .forth файла")
    parser.add_argument(
        "-c", "--conf", type=str, help="Путь к конфигурационному файлу", required=True
    )
    parser.add_argument("forth_file", type=str, help="Путь к файлу .forth")
    args = parser.parse_args()
    file_path = resource_path(args.forth_file)
    conf_path = resource_path(args.conf)
    build_dir = os.path.join(os.path.dirname(file_path), "build")
    main(file_path, build_dir, conf_path)
