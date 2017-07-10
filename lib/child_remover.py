import copy
from typing import Callable

from lib.simple_dft import execute as do_traversal

from lib.simple_matcher import SimpleMatcher


def remove_children(playfield: dict, test: Callable[[object], bool]) -> dict:
    new_playfield = copy.deepcopy(playfield)
    test_host = generate_child_test(test)
    matcher = SimpleMatcher(test_host)
    operation = generate_child_remover(test)
    do_traversal(new_playfield, matcher, operation)
    return new_playfield


def generate_child_test(test: Callable[[object], bool]) -> Callable[[object], bool]:
    def test_host(node:object) -> bool:
        if isinstance(node, list):
            return any(test(x) for x in node)
        else:
            return False

    return test_host


def generate_child_remover(test: Callable[[object], bool] ):
    def do_child_removal(node: list) -> None:
        node[:] = [x for x in node if not test(x)]
    return do_child_removal

