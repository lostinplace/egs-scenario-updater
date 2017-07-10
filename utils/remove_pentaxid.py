import re

from lib.child_remover import remove_children

resource_pattern = re.compile("PentaxidResource")
crystal_pattern = re.compile("[Cc]rystal")


def remove_pentaxid(playfield:dict) -> dict:

    crystal_test = lambda node: isinstance(node, list) and crystal_pattern.match(str(node[0]))
    without_crystals = remove_children(playfield, crystal_test)
    resource_test = lambda node: isinstance(node, dict) and resource_pattern.match(str(node.get('Name')))

    without_resources = remove_children(without_crystals, resource_test)
    return without_resources

