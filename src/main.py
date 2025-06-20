import argparse
import os
from contextlib import redirect_stdout
from pathlib import Path

import yaml  # type: ignore

from src.code_compiler.assembly.assembly import assembly
from src.code_compiler.compiling.compiling import compile_code as compile_code
from src.stack_machine.console_launch import console_launch
from src.stack_machine.debug_launch import debug_launch


def main(cfg_path: str, file_path: str, debug: bool, log: bool) -> None:
    wd = os.path.dirname(os.path.abspath(__file__)) + "/"
    if wd.startswith("/"):
        wd = ""
    build_dir = wd + os.path.dirname(file_path) + "/build/"
    bin_dir = wd + os.path.dirname(file_path) + "/build/bin/"
    compile_code(file_path, build_dir)
    file = Path(file_path)

    conf = yaml.safe_load(open(cfg_path))
    assembly(build_dir, build_dir + "/code", conf["memory_size"])

    if debug:
        debug_launch(conf, build_dir)
    else:
        if log:
            with open(file.with_suffix(".log"), "w") as f:
                with redirect_stdout(f):
                    console_launch(conf, bin_dir)
        else:
            console_launch(conf, bin_dir)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Парсер для конфига и .forth файла")
    parser.add_argument(
        "-c", "--conf", type=str, help="Путь к конфигурационному файлу", required=True
    )
    parser.add_argument("-f", "--forth_file", type=str, help="Путь к файлу .forth")

    parser.add_argument(
        "-d", "--debug", action="store_true", help="Включить режим отладки"
    )
    parser.add_argument(
        "-l", "--log", action="store_true", help="Включить режим отладки"
    )
    args = parser.parse_args()
    main(args.conf, args.forth_file, args.debug, args.log)
