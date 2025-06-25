import yaml  # type: ignore

from src.common import resource_path

with open(resource_path("src/stack_machine/config/config.yaml")) as config_file:
    cfg = yaml.safe_load(config_file)

log_file = cfg["LOG_FILE"]
instruction_file = cfg["INSTRUCTION_FILE"]
microcode_mem_file = cfg["MICRO_COMMAND_MEM_PATH"] + "microcode.bin"
op_table_file = cfg["MICRO_COMMAND_MEM_PATH"] + "op_table.yaml"
source_mc_file = cfg["SOURCE_MC_FILE"]
