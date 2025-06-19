
import yaml  # type: ignore

from src.stack_machine.cpu.mem import DataMem
from .init_cpu import compile_code
from .mc_compiler.compile import compile_micro_command
from .utils.console_layout import ConsoleLayout


def debug_launch(cfg_path: str, build_dir: str) -> None:
    compile_micro_command()
    conf = yaml.safe_load(open(cfg_path))
    io_ports = []
    for i in conf["input_streams"]:
        io_ports.append(i)

    start = compile_code(build_dir + "/code", conf["memory_size"])
    mem = DataMem(io_ports, conf["input_streams"][io_ports[0]])

    limit = conf["limit"]

    console = ConsoleLayout(start, mem, limit)
    console.run()


if __name__ == "__main__":

    cfg_path = "/media/ra/_work/ra/ITMO/CSA/lab4/stack_machine/zalupa.yaml"
    debug_launch(cfg_path, "../build")
