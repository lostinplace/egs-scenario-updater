#!/usr/bin/env python3

from run import build_new_scenario
from utils.launcher_funcs import parse_updater_args, config_message, find_config_file, get_paths

if __name__ == "__main__":
    find_config_file()

    args = parse_updater_args()
    print(args)
    basepath, input_path, output_path = get_paths(vars(args))
    print(config_message.format(basepath, input_path, output_path))

    build_new_scenario(input_path, basepath, output_path)
