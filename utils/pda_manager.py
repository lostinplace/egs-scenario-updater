import csv
from os import makedirs

from os.path import isfile
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

    with open(messages_path, "rb") as messages_file:
        contents = messages_file.read().decode("utf-8")

    return contents.split("\n")


def write_pda(pda: dict, output_scenario_path: str):

    pda_folder_path = pda_folder_format.format(output_scenario_path)
    makedirs(pda_folder_path, exist_ok=True)
    pda_file_path = pda_path_format.format(pda_folder_path)
    with open(pda_file_path, 'w') as outfile:
        yaml.dump(pda, outfile, default_flow_style=False)


def write_messages(messages: list, output_scenario_path: str):

    pda_folder_path = pda_folder_format.format(output_scenario_path)
    makedirs(pda_folder_path, exist_ok=True)
    messages_file_path = pda_messages_path_format.format(pda_folder_path)
    content = "\n".join(messages)
    with open(messages_file_path, 'w') as outfile:
        outfile.write(content)


def construct_basic_pda() -> dict:
    return {
        "Creator": "auto-generated",
        "Chapters": []
    }