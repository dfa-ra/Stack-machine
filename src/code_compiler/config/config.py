import os

import yaml # type: ignore

wd = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(wd, 'config.yaml')) as config_file:
    cfg = yaml.safe_load(config_file)

instruction_file = wd + "/" + cfg['INSTRUCTION_FILE']