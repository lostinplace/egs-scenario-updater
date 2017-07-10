from typing import Callable


class SimpleMatcher(object):

    "biome decorations :x: key value"

    def __init__(self, *args: Callable[[object], bool]) -> bool:
        self.tests = list(args)

    def matches(self, node):
        return any(t(node) for t in self.tests)