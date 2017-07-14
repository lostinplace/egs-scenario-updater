from genericpath import isfile
from os import makedirs

import yaml
from ruamel import yaml

playfield_folder_path_format = "{}/Playfields/{}"
playfield_file_path_format = "{}/playfield.yaml"


def write_playfields(playfield_dict: dict, output_scenario_path: str):
    for k, v in playfield_dict.items():
        playfield_folder = playfield_folder_path_format.format(output_scenario_path, k)
        makedirs(playfield_folder, exist_ok=True)
        playfield_file_path = playfield_file_path_format.format(playfield_folder)
        with open(playfield_file_path, 'w') as outfile:
            yaml.dump(v, outfile, default_flow_style=False)


def get_playfield(playfield_path:str) -> map:
    if not isfile(playfield_path):
        return None

    with open(playfield_path, "rb") as input_stream:
        data = input_stream.read()

    contents = data.decode("utf-8")

    safe_contents = contents.replace("\t", "  ")
    doc = yaml.safe_load(safe_contents)
    return doc

playfield_path_format = "{}/Playfields/{}/playfield.yaml"
