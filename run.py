from functools import reduce
from os.path import exists, isdir
from shutil import copytree, rmtree, move
from sys import argv
from typing import Callable, List, Set, Sequence, Tuple

from lib.rule_based_dft import execute
from utils.capitalize_struct_boolean import generate_struct_capitalization_rule
from utils.mission_builder import construct_playfield_chapter
from utils.nerf_resources import nerf_resources
from utils.pda_manager import load_pda, construct_basic_pda, write_pda, load_pda_messages, \
    reformat_simple_dict_into_message_dict, write_messages
from utils.playfield_manager import get_playfield, playfield_path_format, write_playfields
from utils.remove_pentaxid import generate_crystal_removal_rule, generate_pentaxid_removal_rule
from utils.sector_processing import get_playfields_from_sector_file, update_sector_file


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

        rules = {
            "remove crystals": generate_crystal_removal_rule(),
            "remove pentaxid": generate_pentaxid_removal_rule(),
            "capitalize structs": generate_struct_capitalization_rule()
        }

        rules_executed = execute(rules, playfield)
        resources_nerfed = nerf_resources(rules_executed)

        return resources_nerfed
    return process_playfield


def process_playfield_types(playfield_types:Sequence[str], scenario_path:str, stock_path:str) -> dict:
    playfield_processor = generate_playfield_processor(scenario_path, stock_path)
    results = map(lambda x: (x, playfield_processor(x)), playfield_types)
    out = filter(lambda x: x[1] is not None, results)
    return dict(out)


def process_playfields(scenario_path:str, stock_path: str):
    playfield_name_type_dict: dict = get_playfields_from_sector_file(scenario_path)

    playfield_type_set: Set[str] = set(playfield_name_type_dict.values())

    processed_playfield_type_dict = process_playfield_types(playfield_type_set, scenario_path, stock_path)

    named_transformed_playfields = filter(lambda x: x[1] in processed_playfield_type_dict, playfield_name_type_dict.items())

    missionready_playfields = map(lambda x: (x[0], processed_playfield_type_dict.get(x[1])), named_transformed_playfields)

    chapters = map(lambda x: construct_playfield_chapter(*x), missionready_playfields)

    chapters_filtered = filter(lambda x: x is not None, chapters)
    chapters, message_groups = zip(*chapters_filtered)
    messages = reduce(lambda a, b: {**a, **b}, message_groups)
    renamed_playfields, mapping_dict = manage_playfield_rename(processed_playfield_type_dict)

    return renamed_playfields, mapping_dict, list(chapters), messages


def manage_playfield_rename(playfield_type_dict:dict) -> Tuple[dict, dict]:
    new_names = map(lambda x:(x, "processed_{}".format(x)), playfield_type_dict)
    mapping_dict = dict(new_names)
    renamed_playfields = map(lambda x: (mapping_dict[x], playfield_type_dict[x]), playfield_type_dict)
    result = dict(renamed_playfields)
    return result, mapping_dict


def build_new_scenario(old_scenario_path: str, stock_path: str, new_scenario_path: str):
    # process sectors

    playfields, name_mapping, chapters, messages = process_playfields(old_scenario_path, stock_path)
    if exists(new_scenario_path) and isdir(new_scenario_path):
        rmtree(new_scenario_path)
    copytree(old_scenario_path, new_scenario_path)
    rename_playfield_folders(name_mapping, new_scenario_path)
    write_playfields(playfields, new_scenario_path)
    update_pda(new_scenario_path, chapters)
    update_messages(new_scenario_path, messages)
    update_sector_file(new_scenario_path, name_mapping)


playfield_folder_path_format = "{}/Playfields/{}"


def rename_playfield_folders(name_mapping: dict, scenario_path:str):
    for k,v in name_mapping.items():
        source_path = playfield_folder_path_format.format(scenario_path, k)
        dest_path = playfield_folder_path_format.format(scenario_path, v)
        if isdir(source_path):
            move(source_path, dest_path)


def update_pda(scenario_path:str, chapters:list):
    pda = load_pda(scenario_path)
    if pda is None:
        pda = construct_basic_pda()

    old_chapter_list: list = pda['Chapters']
    old_chapter_list.extend(chapters)
    write_pda(pda, scenario_path)


def update_messages(scenario_path:str, messages:dict):
    old_messages = load_pda_messages(scenario_path)
    if old_messages is None:
        old_messages = {}

    formatted_new_messages = reformat_simple_dict_into_message_dict(messages)

    new_message_dict = {**old_messages, **formatted_new_messages}

    write_messages(new_message_dict, scenario_path)


if __name__ == "__main__":
    args = argv
    input_scenario_path = argv[1]
    print(input_scenario_path)
    stock_data_path = argv[2]
    print(stock_data_path)
    output_scenario_path = argv[3]
    print(output_scenario_path)
    build_new_scenario(input_scenario_path, stock_data_path, output_scenario_path)
