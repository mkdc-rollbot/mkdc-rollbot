import re

from dataclasses import dataclass, field


DICE_REGEX = r"(?P<count>\d+)d(?P<die>\d+)(r\((?P<reroll_list>(\d+\,)*(\d))\))?(?P<keep>k[h|l]\d+)?(\+(?P<add>\d+))?"

@dataclass
class RollCommand:
    dice_type: int
    dice_count: int
    reroll_on: list[int] = field(default_factory=list)
    add: int = 0
    keep_highest: int = 0
    keep_lowest: int = 0


    @classmethod
    def from_regex(cls, dice_roll_string):
        match_groups = re.match(DICE_REGEX, dice_roll_string).groupdict()
        dice_type = int(match_groups['die'])
        count = int(match_groups['count'])
        reroll_list = [] if match_groups['reroll_list'] is None else list(map(int, match_groups['reroll_list'].split(',')))
        keep_highest = 0 if not match_groups['keep'] or 'h' not in match_groups['keep'] else int(match_groups['keep'][2:])
        keep_lowest = 0 if not match_groups['keep'] or 'l' not in match_groups['keep'] else int(match_groups['keep'][2:])
        add = 0 if match_groups['add'] is None else int(match_groups['add'])

        cls.validate(dice_type, count, reroll_list, keep_highest, keep_lowest, add)

        return cls(dice_type, count, reroll_list, add, keep_highest, keep_lowest)

    @staticmethod
    def validate(dice_type, count, reroll_list, keep_highest, keep_lowest, add):
        if any(reroll_value >= dice_type for reroll_value in reroll_list):
            raise ValueError(f"{reroll_list} is invalid for d{dice_type}.")

        if keep_highest > 0 and keep_lowest > 0:
            raise ValueError(f"Got both keep highest and keep lowest.")

        if keep_highest > count or keep_lowest > count:
            raise ValueError(f"Invalid keep value {keep_highest if keep_highest else keep_lowest} for {count} rolls.")

async def parse_roll(roll_description: str) -> RollCommand:
    return RollCommand.from_regex(roll_description)
