import re

from typing import Any, Union

from .system_base import CharacterSheet, RolePlayingSystem, CharacterVariant

class Dnd5e(RolePlayingSystem):
    EXP = 'EXPERTISE'

    def check(self, character: Dnd5ECharacterSheet, skill: str, check_str: str = None) -> int:
        score = character.skill_score(skill)
        roll_result = roll_die(DICE_DICT[CHECK_DIE]) + score
        check_mod: Dnd5eCheckMod = CHECK_MODS.get(check_str, Dnd5eCheckMod.NONE) if check_str else Dnd5eCheckMod.NONE
        if check_mod == Dnd5eCheckMod.NONE:
            return roll_result

        alt_roll = roll_die(DICE_DICT[CHECK_DIE]) + score
        if check_mod == Dnd5eCheckMod.ADVANTAGE:
            return max(roll_result, alt_roll)
        elif check_mod == Dnd5eCheckMod.DISADVANTAGE:
            return min(roll_result, alt_roll)
        else:
            raise ValueError(f'Got unknown Dnd5eCheckMod: {check_mod}')

    @staticmethod
    def parse(desc: str) -> int:
        processed_desc = re.match(DICE_ROLL_REGEX, desc)
        if not processed_desc:
            raise ValueError(f"Bad dice roll description {desc}")
        die, rolls = DICE_DICT[processed_desc['Dice']], processed_desc['Times']
        if not rolls:
            rolls = 1
        roll_sum = 0
        for roll in range(rolls):
            roll_sum += roll_die(die)

        return roll_sum

    def character_sheet(self, args_list: list[str]) -> (Dnd5ECharacterSheet, str):
        name = args_list.pop(0)
        level = int(args_list.pop(0))
        stats = [int(stat) for stat in args_list[0:len(STATS)]]
        proficiencies = [prof for prof in args_list[len(STATS): args_list.index(self.EXP) if self.EXP in args_list else len(args_list)]]
        expertise = None
        if self.EXP in args_list:
            expertise = args_list[args_list.index(self.EXP)+1:]
        return Dnd5ECharacterSheet(name, level, stats, proficiencies, expertise), name

    def __str__(self) -> str:
        return 'Dungeons and Dragons 5th Edition (2014)'

    def key(self):
        return 'dnd5e'
