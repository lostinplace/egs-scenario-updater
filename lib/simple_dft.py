from typing import Callable

from lib.simple_matcher import SimpleMatcher


def execute(node, matcher:SimpleMatcher, operation:Callable[[object], None]):
    if isinstance(node, dict):
        for k,v in node.items():
            execute(v, matcher, operation)
            if matcher.matches(v):
                operation(v)
    elif isinstance(node, list):
        for i in node:
            execute(i, matcher, operation)
            if matcher.matches(i):
                operation(node)
    else:
        if matcher.matches(node):
            operation(node)