from functools import reduce
from os.path import exists, isdir
from shutil import copytree, rmtree
from typing import Callable, List, Set

from utils.mission_builder import construct_playfield_chapter
from utils.nerf_resources import nerf_resources
from utils.pda_manager import load_pda, construct_basic_pda, write_pda
from utils.playfield_manager import get_playfield, playfield_path_format, write_playfields
from utils.remove_pentaxid import remove_pentaxid
from utils.sector_processing import parse_sectors


def generate_playfield_processor(scenario_path: str, stock_path: str) -> Callable[[str], dict]:

    def process_playfield(playfield_type: str) -> dict:
        """
        processes an individual playfield
        :param playfield_name:
        :param playfield_type: the folder where you expect to find it
        :return:  playfield, chapter, messages
        """

        scenario_playfield_path = playfield_path_format.format(scenario_path, playfield_type)
        playfield = get_playfield(scenario_playfield_path)
        if playfield is None:
            stock_playfield_path = playfield_path_format.format(stock_path, playfield_type)
            playfield = get_playfield(stock_playfield_path)
            if playfield is None:
                return None

        pentaxid_removed = remove_pentaxid(playfield)
        resources_nerfed = nerf_resources(pentaxid_removed)
        return resources_nerfed
    return process_playfield


def process_playfield_types(playfield_types:List[str], scenario_path:str, stock_path:str) -> dict:
    playfield_processor = generate_playfield_processor(scenario_path, stock_path)
    results = map(lambda x: (x, playfield_processor(x)), playfield_types)
    return dict(results)


blocked_types = set("Sun")


def process_playfields(scenario_path:str, stock_path: str):
    sectors = parse_sectors(scenario_path)
    sector_names, sector_types = zip(*sectors)
    sector_type_set: Set[str] = set(sector_types)
    valid_playfield_types = filter(lambda x: x[1] not in blocked_types, sector_type_set)
    playfield_type_dict = process_playfield_types(list(valid_playfield_types), scenario_path, stock_path)
    resolved_playfields = map(lambda x: (x[0], playfield_type_dict.get(x[1])), sectors)
    chapters = map(lambda x: construct_playfield_chapter(*x), resolved_playfields)
    chapters_filtered = filter(lambda x: x is not None, chapters)
    chapters, message_groups = zip(*chapters_filtered)
    messages = reduce(lambda a, b: {**a, **b}, message_groups)
    return playfield_type_dict, list(chapters), messages


def build_new_scenario(old_scenario_path: str, stock_path: str, new_scenario_path: str):
    playfields, chapters, messages = process_playfields(old_scenario_path, stock_path)
    if exists(new_scenario_path) and isdir(new_scenario_path):
        rmtree(new_scenario_path)
    copytree(old_scenario_path, new_scenario_path)
    write_playfields(playfields, new_scenario_path)
    update_pda(new_scenario_path, chapters)


def update_pda(scenario_path:str, chapters:list):
    pda = load_pda(scenario_path)
    if pda is None:
        pda = construct_basic_pda()

    old_chapter_list: list = pda['Chapters']
    old_chapter_list.extend(chapters)
    write_pda(pda, scenario_path)


if __name__ == "__main__":
    # execute only if run as a script
    "1"