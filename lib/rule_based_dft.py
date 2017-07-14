from typing import Callable, Dict, Union, Sequence

from functools import reduce

from lib.simple_rule import SimpleRule

rule_dict = Dict[str, SimpleRule]
rule_or_rule_dict = Union[SimpleRule, rule_dict]

default_key = "default"


def execute(rules: rule_or_rule_dict, node) -> object:

    if isinstance(rules, dict):
        rules_dict: rule_dict = rules
    elif isinstance(rules, Sequence):
        rules_dict: rule_dict = dict(enumerate(rules))
    else:
        rules_dict: rule_dict = {default_key: rules}

    def executor(x):
        return execute(rules_dict, x)

    if isinstance(node, dict):
        this_node = {}
        for k, v in node.items():
            this_node[k] = execute(rules_dict, v)
    elif isinstance(node, list):
        rules_executed = map(executor, node)
        this_node = list(rules_executed)
    else:
        this_node = node

    result = reduce(lambda memo, a_rule: a_rule.execute(memo), rules_dict.values(), this_node)

    return result
