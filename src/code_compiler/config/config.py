import yaml  # type: ignore

from src.common import resource_path

with open(resource_path("src/code_compiler/config/config.yaml")) as config_file:
    cfg = yaml.safe_load(config_file)

instruction_file = cfg["INSTRUCTION_FILE"]
