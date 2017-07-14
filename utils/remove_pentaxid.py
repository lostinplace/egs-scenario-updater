import re

from lib.child_removal_rule import ChildRemovalRule

resource_pattern = re.compile("PentaxidResource")
crystal_pattern = re.compile("[Cc]rystal")


def generate_pentaxid_removal_rule():
    return ChildRemovalRule(is_pentaxid_resource)


def is_pentaxid_resource(node: object) -> bool:
    return isinstance(node, dict) and resource_pattern.match(str(node.get('Name')))


def generate_crystal_removal_rule():
    return ChildRemovalRule(is_crystal_decoration)


def is_crystal_decoration(node:object) -> bool:
    return isinstance(node, list) and crystal_pattern.match(str(node[0]))
