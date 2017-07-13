import csv
from os import makedirs

from os.path import isfile
from typing import List, Sequence

from functools import reduce
from ruamel import yaml

pda_folder_format = "{}/Extras/PDA"
pda_path_format = "{}/PDA.yaml"
pda_messages_path_format = "{}/PDA.csv"


def load_pda(scenario_path: str="", pda_path: str=""):
    if pda_path is "":
        pda_folder_path = pda_folder_format.format(scenario_path)
        pda_path = pda_path_format.format(pda_folder_path)

    if not isfile(pda_path):
        return None

    with open(pda_path, "rb") as input_stream:
        data = input_stream.read()

    contents = data.decode("utf-8")
    doc = yaml.safe_load(contents)
    return doc


def load_pda_messages(scenario_path:str, messages_path: str=""):
    if messages_path is "":
        pda_folder_path = pda_folder_format.format(scenario_path)
        messages_path = pda_messages_path_format.format(pda_folder_path)

    if not isfile(messages_path):
        return None

    with open(messages_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        output = list(reader)

    header_vals: Sequence = output.pop(0)

    def to_dict(cells):
        result = {}
        for i,value in enumerate(cells):
            key = header_vals[i]
            result[key] = value

        return {result['KEY']: result} if result else None

    messages = map(to_dict, output)
    valid_messages = filter(lambda x: x is not None, messages)
    result = reduce(lambda a,b: {**a, **b}, valid_messages)

    return result


def write_pda(pda: dict, output_scenario_path: str):

    pda_folder_path = pda_folder_format.format(output_scenario_path)
    makedirs(pda_folder_path, exist_ok=True)
    pda_file_path = pda_path_format.format(pda_folder_path)
    with open(pda_file_path, 'w') as outfile:
        yaml.dump(pda, outfile, default_flow_style=False)


def write_messages(messages: dict, output_scenario_path: str):
    pda_folder_path = pda_folder_format.format(output_scenario_path)
    messages_path = pda_messages_path_format.format(pda_folder_path)

    fieldnames = ["KEY", "English", "Deutsch"]
    with open(messages_path, 'w', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for k in messages:
            row = messages[k]
            writer.writerow(row)


def reformat_simple_dict_into_message_dict(messages:dict):
    result = {}
    for (k, v) in messages.items():
        result[k] = {"KEY": k, "English": v}

    return result


def construct_basic_pda() -> dict:
    return {
        "Creator": "auto-generated",
        "Chapters": []
    }