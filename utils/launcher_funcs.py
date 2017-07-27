import os
from argparse import Namespace
from typing import Dict, Tuple


def parse_updater_args() -> Namespace:
    import argparse

    description = """transforms a scenario file, if basepath or config path are not provided, it searches for \
    .updater-config
    """

    parser = argparse.ArgumentParser(prog='python run.py')
    basepath_help = """path to the game folder, or the content folder containing all prefabs and scenerios"""

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--basepath', help=basepath_help)
    group.add_argument('--config-path', help='path to a config file specifying the basepath')
    parser.add_argument('source', help='name of the source scenario')
    parser.add_argument('dest', help='name of the destination scenario')
    return parser.parse_args()


def read_config_file(path: str):
    with open(path, 'r') as f:
        return f.read().strip()


config_message = """\
Executing with:
    Content Folder Path:  {}
    Input Scenario Path:  {}
    Output Scenario Path: {}
"""


def find_config_file():
    import os

    current_folder = './'
    while os.path.exists(current_folder) and os.path.isdir(current_folder):
        file_path = current_folder + '.updater-config'
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return file_path
        current_folder += '../'


def identify_and_resolve_content_folder(basepath: str) -> str:
    if not os.path.isdir(basepath):
        return None
    if os.path.isdir(basepath+'/Content'):
        return os.path.isdir(basepath+'/Content')
    elif os.path.isdir(basepath+'/Scenarios'):
        return basepath


def get_paths(arg_dict: Dict[str, str]) -> Tuple[str, str, str]:

    basepath = arg_dict.get('basepath', [])
    config = arg_dict.get('config-path', None)
    if basepath is not None:
        pass
    elif config is not None:
        basepath = read_config_file(config)
    elif find_config_file() is not None:
        config_path = find_config_file()
        print("using config file at: {}".format(os.path.realpath(config_path)))
        basepath = read_config_file(config_path)
    else:
        raise Exception("couldn't find basepath or configuration file")

    content_folder_path = identify_and_resolve_content_folder(basepath)

    source_string = arg_dict['source']
    if os.path.isdir(source_string):
        input_scenario_path = source_string
    else:
        input_scenario_path = content_folder_path + '/Scenarios/' + arg_dict['source']

    dest_string = arg_dict['dest']
    dirname = os.path.dirname(dest_string)
    if os.path.exists(dirname) and os.path.isdir(dirname):
        output_scenario_path = dest_string
    else:
        output_scenario_path = content_folder_path + '/Scenarios/' + dest_string

    return os.path.realpath(content_folder_path), \
           os.path.realpath(input_scenario_path), \
           os.path.realpath(output_scenario_path)