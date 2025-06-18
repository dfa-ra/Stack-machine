import os

import yaml

from .cpu.mem import DataMem
from .init_cpu import compile_code
from .mc_compiler.compile import compile_micro_command
from .utils.console_layout import ConsoleLayout


def debug_launch(cfg_path, build_dir):
    compile_micro_command()
    conf = yaml.safe_load(open(cfg_path))
    io_ports = []
    for i in conf["input_streams"]:
        io_ports.append(i)

    start = compile_code(build_dir + "/examples", conf["memory_size"])
    mem = DataMem(io_ports, conf["input_streams"][io_ports[0]])

    console = ConsoleLayout(start, mem)
    console.run()


if __name__ == "__main__":

    cfg_path = "/media/ra/_work/ra/ITMO/CSA/lab4/stack_machine/zalupa.yaml"
    debug_launch(cfg_path, "../build")
