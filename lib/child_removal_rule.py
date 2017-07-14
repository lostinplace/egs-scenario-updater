
from itertools import filterfalse
from typing import Callable

from lib.simple_rule import SimpleRule


class ChildRemovalRule(SimpleRule):

    def __init__(self, child_identifier: Callable[[object], bool]):

        def evaluator(node: object):
            return isinstance(node, list) and any(map(child_identifier, node))

        conditions = [evaluator]
        effects = [lambda node: list(filterfalse(child_identifier, node))]
        SimpleRule.__init__(self, conditions, effects)
