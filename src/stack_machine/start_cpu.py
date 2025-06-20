import argparse
import os

import yaml  # type: ignore

from src.stack_machine.console_launch import console_launch


def main(bin_path: str, conf_path: str, start_addr: int) -> None:
    conf = yaml.safe_load(open(conf_path))
    console_launch(conf, bin_path, start_addr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Парсер для конфига и .forth файла")
    parser.add_argument(
        "-c", "--conf", type=str, help="Путь к конфигурационному файлу", required=True
    )
    parser.add_argument(
        "-b", "--bin_path", type=str, help="Путь к папке bin", required=True
    )
    parser.add_argument(
        "-a", "--start_addr", type=int, help="Точка входа в программу", required=True
    )

    args = parser.parse_args()
    wd = os.path.dirname(os.path.abspath(__file__)) + "/"
    if args.bin_path.startswith("/"):
        wd = ""
    bin_path = wd + args.bin_path
    conf_path = wd + args.conf
    main(bin_path, conf_path, args.start_addr)
