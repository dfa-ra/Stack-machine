from src.stack_machine.cpu import Cpu
from src.stack_machine.cpu.mem import DataMem, InstructionMem
from src.stack_machine.os import parse_exec
from src.stack_machine.logging.logger import logger
from src.stack_machine.mc_compiler.compile import compile_micro_command


def console_launch(conf, exec_path: str) -> None:  # type: ignore
    compile_micro_command()
    io_ports = []
    for i in conf["input_streams"]:
        io_ports.append(i)

    data_memory, instruction_data, start_address = parse_exec(
        exec_path, int(conf["memory_size"])
    )

    mem = DataMem(io_ports, conf["input_streams"][io_ports[0]], data_memory)
    i_mem: InstructionMem = InstructionMem(instruction_data)

    _cpu = Cpu(13, mem, i_mem, start_address)

    logger_ = logger(_cpu, conf["reports"], instruction_data)

    limit = conf["limit"]

    logger_.run_binary()
    while _cpu.running and _cpu.tick_count < limit:
        _cpu.tick(logger_.each_tick_logs, logger_.command)
    logger_.run_assert()


if __name__ == "__main__":
    cfg_path = "/media/ra/_work/ra/ITMO/CSA/lab4/stack_machine/zalupa.yaml"
    console_launch(cfg_path, "../build/bin")
