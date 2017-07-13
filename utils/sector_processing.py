from itertools import chain
from typing import Dict

import yaml


def extract_sector_names(sector: dict) -> list:
    playfields:list[list[str]] = sector['Playfields']
    playfield_names = [(x[1], x[2]) for x in playfields]
    return playfield_names

sector_file_path_format = "{}/Sectors/Sectors.yaml"


def flatmap(groups):
    for group in groups:
        for item in group:
            if item is not None:
                yield item


def get_playfields_from_sector_file(scenario_path:str) -> Dict[str, str]:
    sector_file_path = sector_file_path_format.format(scenario_path)
    with open(sector_file_path, "rb") as stream:
        contents = stream.read()
        data = contents.decode("utf-8")

    doc = yaml.load(data)

    if isinstance(doc, list):
        sectors: list = doc
    else:
        sectors: list = doc.get('Sectors')

    playfield_groups = map(lambda x: x['Playfields'], sectors)
    playfields = flatmap(playfield_groups)
    playfield_name_types = map(lambda x: (x[1], x[2]), playfields)

    return dict(playfield_name_types)


def update_sector_file(new_scenario_path:str, new_mapping:dict):
    sector_file_path = sector_file_path_format.format(new_scenario_path)
    with open(sector_file_path, "rb") as stream:
        contents = stream.read()
        data = contents.decode("utf-8")

    doc = yaml.load(data)

    if isinstance(doc, list):
        sectors: list = doc
    else:
        sectors: list = doc.get('Sectors')

    for sector in sectors:
        for playfield in sector['Playfields']:
            playfield_type = playfield[2]
            if playfield_type in new_mapping:
                playfield[2] = new_mapping[playfield_type]

    with open(sector_file_path, 'w') as outfile:
        yaml.dump(doc, outfile, default_flow_style=False)


