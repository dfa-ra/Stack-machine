import argparse

import yaml  # type: ignore

from src.common.common import resource_path
from src.stack_machine.console_launch import console_launch


def main(exec_path: str, conf_path: str) -> None:
    conf = yaml.safe_load(open(conf_path))
    console_launch(conf, exec_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Парсер для конфига и .forth файла")
    parser.add_argument(
        "-c", "--conf", type=str, help="Путь к конфигурационному файлу", required=True
    )
    parser.add_argument(
        "-b", "--bin_path", type=str, help="Путь к папке bin", required=True
    )

    args = parser.parse_args()

    bin_path = resource_path(args.bin_path)
    conf_path = resource_path(args.conf)
    main(bin_path, conf_path)
