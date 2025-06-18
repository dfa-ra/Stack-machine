import argparse
import os

from src.code_compiler.compile_app import compile_code
from src.stack_machine.console_launch import console_launch
from src.stack_machine.debug_launch import debug_launch


def main(conf, file_path, debug):
    wd = os.path.dirname(os.path.abspath(__file__))
    build_dir = wd + "/" + os.path.dirname(file_path) + '/build/'
    print(build_dir)
    compile_code(file_path, build_dir)
    if debug:
        debug_launch(conf, build_dir)
    else:
        console_launch(conf, build_dir)
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Парсер для конфига и .forth файла")
    parser.add_argument('-c', '--conf', type=str, help='Путь к конфигурационному файлу', required=True)
    parser.add_argument('forth_file', type=str, help='Путь к файлу .forth')
    parser.add_argument('-d', '--debug', action='store_true', help='Включить режим отладки')
    args = parser.parse_args()
    main(args.conf, args.forth_file, args.debug)
