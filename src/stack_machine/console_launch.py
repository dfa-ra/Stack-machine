from src.stack_machine.cpu.mem import DataMem
from src.stack_machine.init_cpu import init_cpu
from src.stack_machine.logging.logger import logger
from src.stack_machine.mc_compiler.compile import compile_micro_command


def console_launch(conf, bin_dir: str) -> None:  # type: ignore
    compile_micro_command()
    io_ports = []
    for i in conf["input_streams"]:
        io_ports.append(i)
    bin_path_data_memory = bin_dir + "/data_memory.bin"
    bin_path_instruction_memory = bin_dir + "/instruction_memory.bin"
    mem = DataMem(io_ports, conf["input_streams"][io_ports[0]], bin_path_data_memory)

    _cpu = init_cpu(mem, bin_path_instruction_memory)
    logger_ = logger(_cpu, conf["reports"], bin_path_instruction_memory)

    limit = conf["limit"]

    logger_.run_binary()
    while _cpu.running and _cpu.tick_count < limit:
        _cpu.tick(logger_.each_tick_logs, logger_.command)
    logger_.run_assert()


if __name__ == "__main__":
    cfg_path = "/media/ra/_work/ra/ITMO/CSA/lab4/stack_machine/zalupa.yaml"
    console_launch(cfg_path, "../build/bin")
