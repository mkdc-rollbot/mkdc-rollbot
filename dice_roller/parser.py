import re

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class RollComand:
    dice_type: int
    dice_count: int
    reroll_on: list[int] = field(default_factory=list)
    add: int = 0
    keep_highest: int = 0
    keep_lowest: int = 0

    dice_regex: ClassVar(str) = r"(?P<count>\d+)d(?P<die>\d+)(r\[(?P<reroll_list>(\d+\,)*(\d))\])?(?P<keep>k[h|l]\d+)?(\+(?P<add>\d+))?"

    @classmethod
    def from_regex(cls, dice_roll_string):
        match_groups = re.match(cls.dice_regex, dice_roll_string).groupdict()
        dice_type = match_groups['die']
        count = match_groups['count']
        reroll_list = [] if match_groups['reroll_list'] is None else match_group['reroll_list'].split(',')
        keep_highest = 0 if 'h' not in match_groups['keep'] else int(match_groups['keep'][2:])
        keep_lowest = 0 if 'l' not in match_groups['keep'] else int(match_groups['keep'][2:])
        add = match_groups['add']

        cls.validate(dice_type, count, reroll_list, keep_highest, keep_lowest, add)

        return cls(dice_type, count, reroll_list, add, keep_highest, keep_lowest)

    @staticmethod
    def validate(dice_type, count, reroll_list, keep_highest, keep_lowest, add):
        if any(reroll_value >= dice_type for reroll_value in dice_type):
            raise ValueError(f"{reroll_value} is invalid reroll value for d{dice_type}.")

        if keep_highest > 0 and keep_lowest > 0:
            raise ValueError(f"Got both keep highest and keep lowest.")

        if keep_highest > count or keep_lowest > count:
            raise ValueError(f"Invalid keep value {keep highest if keep_highest else keep_lowest} for {count} rolls.")

def parse_roll(roll_description: str) -> RollCommand:
    return RollCommand.from_regex(roll_description)
