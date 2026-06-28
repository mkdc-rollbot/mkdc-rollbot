import re

from enum import Enum, Flag, auto
from typing import Any, Union

from src.system_base import CharacterSheet, RolePlayingSystem, CharacterVariant

from collections import namedtuple
from random import randint


Die = namedtuple('Die', ['min', 'max'])


def roll_die(die: Die) -> int:
    return randint(*die)

GenerateType = Union[
    int,
    tuple[int, int],
    tuple[int, str],
    tuple[int, int, str],
]

def generate_dice(to_generate: list[GenerateType]) -> dict[str, Die]:
    dice_dict = {}
    for die_data in to_generate:
        match die_data:
            case int() as max_val:
                new_key = str(max_val)
                new_val = Die(1, max_val)
            case (min_val, max_val) if isinstance(min_val, int) and isinstance(max_val, int):
                new_key = f'{min_val}-{max_val}'
                new_val = Die(min_val, max_val)
            case (max_val, name) if isinstance(max_val, int) and isinstance(name, str):
                new_key = name
                new_val = Die(1, max_val)
            case (min_val, max_val, name) if isinstance(min_val, int) and isinstance(max_val, int) and isinstance(name, str):
                new_key = name
                new_val = Die(min_val, max_val)
            case _:
                raise ValueError
        dice_dict[new_key] = new_val
    return dice_dict

############################################
# CONSTANTS
############################################

# Define the Die struct and dice used in DnD

DND_DICE = [4, 6, 8, 10, (100, '%'), 12, 20]
DICE_DICT = generate_dice(DND_DICE)
CHECK_DIE = '20'

DICE_PATTERN = '|'.join(sorted(DICE_DICT.keys(), key=len, reverse=True))
DICE_ROLL_REGEX = rf"(?P<Times>\d*)d(?P<Dice>{DICE_PATTERN})"

class SkillModifier(Flag):
    PROFICIENCY = auto()
    EXPERTISE = auto()

class Dnd5eCheckMod(Enum):
    NONE = 0
    ADVANTAGE = 1
    DISADVANTAGE = 2

CHECK_MODS: dict[str, Dnd5eCheckMod] = {
    'advantage': Dnd5eCheckMod.ADVANTAGE,
    'disadvantage': Dnd5eCheckMod.DISADVANTAGE
}

############################################
# UTILITY CLASSES
############################################

class Stat:
    def __init__(self, score: int):
        self.score = score

    @property
    def modifier(self) -> int:
        return int((self.score - 10) // 2)


class Skill:
    def __init__(self, stat: Stat, modifier: SkillModifier):
        self.stat = stat
        self.modifier = modifier

    def score(self, prof_bonus: int) -> int:
        prof_multiplier = 0
        if SkillModifier.PROFICIENCY in self.modifier:
            prof_multiplier += 1
            if SkillModifier.EXPERTISE in self.modifier:
                prof_multiplier += 1
        return self.stat.modifier + (prof_bonus * prof_multiplier)

STATS = ['str', 'dex', 'con', 'int', 'wis', 'cha']
SKILLS = {
    'acrobatics': 'dex',
    'animal handling': 'wis',
    'arcana': 'int',
    'athletics': 'str',
    'deception': 'cha',
    'history': 'int',
    'insight': 'wis',
    'intimidation': 'cha',
    'investigation': 'int',
    'medicine': 'wis',
    'nature': 'int',
    'perception': 'wis',
    'performance': 'cha',
    'persuasion': 'cha',
    'religion': 'int',
    'sleight of hand': 'dex',
    'stealth': 'dex',
    'survival': 'wis'
}

# =======================
# CHARACTER SHEET SCHEMA
# =======================

SCHEMA = {
    'name': str,
    'level': int,
    'stats': {stat: int for stat in STATS},
    'skills': {skill: int for skill in SKILLS},
}

class Dnd5ECharacterVariant(CharacterVariant):
    def validate_diffs(self, diffs: dict[str, Any]):
        if not diffs:
            raise ValueError('Empty diff')
        for key, value in diffs.items():
            split_key = key.split('.')
            schema = SCHEMA
            for current_key in split_key:
                if current_key not in schema.keys():
                    raise KeyError(f'Key {current_key} in {key} is not part of the schema.')
                schema = schema[current_key]
            if not isinstance(value, schema):
                raise ValueError(f'Value for {key} should be of type {schema}, got {type(value)}.')

    def parse_diffs(self, diffs: dict[str, Any]):
        parsed_diffs = {}
        for key, value in diffs.items():
            split_key = key.split('.')
            current_diffs = parsed_diffs
            for current_key in split_key[:-1]:
                if current_key not in current_diffs.keys():
                    current_diffs[current_key] = dict()
                current_diffs = current_diffs[current_key]
            current_diffs[current_key] = value
        return parsed_diffs


class Dnd5ECharacterSheet(CharacterSheet):
    def __init__(self, name: str, level: int, stat_scores: list[int], proficiencies: list[str], expertise: list[str] = None):
        assert len(stat_scores) == len(STATS) and all([1 <= stat <= 20 for stat in stat_scores])
        self._stats = {stat: Stat(score) for stat, score in zip(STATS, stat_scores)}
        self.name = name
        self.level = level
        modifiers: dict[str, SkillModifier] = {skill: SkillModifier(0) for skill in SKILLS.keys()}
        for skill in proficiencies:
            modifiers[skill] |= SkillModifier.PROFICIENCY
        if expertise:
            for skill in expertise:
                assert skill in proficiencies
                modifiers[skill] |= SkillModifier.EXPERTISE
        self._skills = {skill: Skill(self._stats[stat], modifiers[skill]) for skill, stat in SKILLS.items()}

    @property
    def proficiency_modifier(self):
        return 2 + (self.level - 1) // 4

    def skill_score(self, skill):
        assert skill in SKILLS.keys()
        return self._skills[skill].score(self.proficiency_modifier)

    @classmethod
    def fromJson(cls, json: dict[str: Any]):
        name = json['name']
        level = json['level']
        stats = []
        for stat in json['stats']:
            stats.append(json['stats'][stat])
        skills = {}
        for skill in json['skills']:
            skills[skill] =int(json['skills'][skill])
        proficiencies = [skill for skill, mod in skills.items() if mod & SkillModifier.PROFICIENCY.value]
        expertise = [skill for skill, mod in skills.items() if mod & SkillModifier.EXPERTISE.value]
        return cls(name, level, stats, proficiencies, expertise)

    def apply_diff(self, variant: Dnd5ECharacterVariant):
        if 'name' in variant:
            self.name = variant['name']
        if 'level' in variant:
            self.level = variant['level']
        if 'stats' in variant:
            for stat in variant['stats']:
                self._stats[stat] = Stat(variant['stats'][stat])
        if 'skills' in variant:
            for skill in variant['skills']:
                self._skills[skill].modifier = SkillModifier(int(variant['skills'][skill]))

    def __repr__(self):
        character_str: str = ''
        character_str += f'Name: {self.name}\n'
        character_str += f'Level: {self.level}\n'
        character_str += f'Stats: {'\t\n'.join([f'{stat}: {s.score}' for stat, s in self._stats.items()])}'
        return character_str

    def toJson(self):
        json = {'name': self.name,
                'level': self.level,
                'stats': {name: stat.score for name, stat in self._stats.items()},
                'skills': {name: skill.modifier.value for name, skill in self._skills.items()}
                }
        return json

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
        return 'Dungeons and Dragons 5th Edition'
