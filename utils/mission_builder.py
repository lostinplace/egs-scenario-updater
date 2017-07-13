import re
from copy import deepcopy
from functools import reduce
from typing import List, Dict, Tuple

separation_pattern = re.compile('[A-Z]*[a-z]*[^A-Z]?')


def format_group_name(group_name:str) -> str:
    without_ts = group_name.replace("TS", "TradingStation")
    elements = re.findall(separation_pattern, without_ts)
    return " ".join(elements)


def get_pois(playfield:dict) -> List[dict]:
    pois: Dict[str, List[dict]] = playfield.get('POIs', {})
    random_pois: List[dict] = pois.get('Random', [])
    return random_pois


def extract_poi_names(pois:List[dict]) -> List[Tuple[str,str]]:
    group_names = map(lambda x: x.get('GroupName'), pois)
    appropriate = filter(lambda x: "TS" not in x, group_names)
    formatted_names = map(lambda x: (x, format_group_name(x)), appropriate)
    return list(formatted_names)

task_title_id_format = "taskCapture{}"
task_title_format = "Capture 1 {}"
action_title_id_format = "actionCapture{}"
action_title_format = "Take Control of a {}"
action_description_id_format = "actionDescription{}"
action_description_format = "Destroy the core block on a {} and replace it with one of your own"
completion_message_id_format = "captured{}"
completion_message_format = "{} Captured"

task_structure = {
    "TaskTitle": '',
    "Rewards":{
        "Item": "PentaxidOre",
        "Count": 5
    },
    "Actions":[]
}

action_structure = {
    "ActionTitle":'',
    "Description": '',
    "Check": "BlocksPlaced",
    "Names": [ ],
    "Types": [ "Core" ],
    "CompletedMessage": "",
}


def generate_conquer_task(formatted_name:Tuple[str, str]) -> Tuple[dict, dict]:
    task_title_id = task_title_id_format.format(formatted_name[0])
    task_title = task_title_format.format(formatted_name[1])
    action_title_id = action_title_id_format.format(formatted_name[0])
    action_title = action_title_format.format(formatted_name[1])
    action_description_id = action_description_id_format.format(formatted_name[0])
    action_description = action_description_format.format(formatted_name[1])
    completion_message_id = completion_message_id_format.format(formatted_name[0])
    completion_message = completion_message_format.format(formatted_name[1])

    out = deepcopy(task_structure)
    out['TaskTitle'] = task_title_id

    action = deepcopy(action_structure)
    action['ActionTitle'] = action_title_id
    action['Names'].append(formatted_name[0])
    action['Description'] = action_description_id
    action['CompletedMessage'] = completion_message_id

    messages = {
        task_title_id: task_title,
        action_title_id: action_title,
        action_description_id: action_description,
        completion_message_id: completion_message,
    }

    out['Actions'].append(action)
    return out, messages

chapter_title_id_format = "chapter{}"
chapter_title_format = "Capture facilities at {}"
chapter_description_id_format = "chapterDescription{}"
chapter_description_format = "Gather warp fuel by conquering facilities at {}"
chapter_completion_id_format = "chapterDescription{}"
chapter_completion_format = "Gather warp fuel by conquering facilities at {}"

chapter_structure = {
    "ChapterTitle": "",
    "Category": "FactionMission",
    "Description": "",
    "PlayerLevel": 1,
    "Visibility": "Always",
    "Rewards": [
        {
            "Item": "GoldCoins",
            "Count": 100
        }
    ],
    "CompletedMessage": "",
    "Tasks":[]
}


def construct_playfield_chapter(playfield_name: str, playfield: dict) -> Tuple[dict, dict]:
    if playfield is None or playfield.get('UseFixed'):
        return None
    out = deepcopy(chapter_structure)
    chapter_title_id = chapter_title_id_format.format(playfield_name.replace(" ", ""))
    chapter_title = chapter_title_format.format(playfield_name)
    chapter_description_id = chapter_description_id_format.format(playfield_name.replace(" ", ""))
    chapter_description = chapter_description_format.format(playfield_name)
    chapter_completion_id = chapter_completion_id_format.format(playfield_name.replace(" ", ""))
    chapter_completion = chapter_completion_format.format(playfield_name)

    out["ChapterTitle"] = chapter_title_id
    out["Description"] = chapter_description_id
    out["CompletedMessage"] = chapter_completion_id

    chapter_messages = {
        chapter_title_id: chapter_title,
        chapter_description_id: chapter_description,
        chapter_completion_id: chapter_completion
    }

    pois = get_pois(playfield)
    poi_names = extract_poi_names(pois)
    task_results = map(generate_conquer_task, poi_names)
    task_result_list = list(task_results)
    if not task_result_list:
        return None

    tasks, messages = zip(*task_result_list)
    out["Tasks"] = list(tasks)

    message_dict = reduce(lambda a,b: {**a, **b}, messages, chapter_messages)

    return out, message_dict




