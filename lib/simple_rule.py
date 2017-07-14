from typing import Callable, Union, List, Sequence

from functools import reduce

condition = Callable[[object], bool]
condition_or_condition_sequence = Union[condition, Sequence[condition]]

effect = Callable[[object], object]
effect_or_effect_sequence = Union[effect, Sequence[effect]]


class SimpleRule(object):

    def __init__(self, conditions: condition_or_condition_sequence, effects:effect_or_effect_sequence, name=""):
        self.condition_list = conditions if isinstance(conditions, Sequence) else list([conditions])
        self.effect_list = effects if isinstance(effects, Sequence) else list([effects])
        self.name = name

    def execute(self, value: object):
        if any(map(lambda the_condition: the_condition(value), self.condition_list)):
            result = reduce(lambda memo, the_effect: the_effect(memo), self.effect_list, value)
            return result
        else:
            return value
