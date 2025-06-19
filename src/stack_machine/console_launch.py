import yaml  # type: ignore

from src.stack_machine.cpu.mem import DataMem
from .init_cpu import compile_code, init_cpu
from .logging.logger import logger
from .mc_compiler.compile import compile_micro_command


def console_launch(cfg_path: str, build_dir: str) -> None:
    compile_micro_command()
    conf = yaml.safe_load(open(cfg_path))
    io_ports = []
    for i in conf["input_streams"]:
        io_ports.append(i)

    start = compile_code(build_dir + "/code", conf["memory_size"])
    mem = DataMem(io_ports, conf["input_streams"][io_ports[0]])

    _cpu = init_cpu(start, mem)
    logger_ = logger(_cpu, conf["reports"])

    limit = conf["limit"]

    logger_.run_binary()
    while _cpu.running and _cpu.tick_count < limit:
        _cpu.tick(logger_.each_tick_logs, logger_.command)
    logger_.run_assert()


if __name__ == "__main__":
    cfg_path = "/media/ra/_work/ra/ITMO/CSA/lab4/stack_machine/zalupa.yaml"
    console_launch(cfg_path, "../build")
