from rollbot.src.system.system_base import CharacterSheet, RolePlayingSystem, Die, roll_die
from enum import Enum, Flag, auto

import re

############################################
# CONSTANTS
############################################

# Define the Die struct and dice used in DnD
d4 = Die(1, 4)
d6 = Die(1, 6)
d8 = Die(1, 8)
d10 = Die(1, 10)
d00 = Die(1, 100)
d12 = Die(1, 12)
d20 = Die(1, 20)

DICE_DICT = {
    '4': d4,
    '6': d6,
    '8': d8,
    '10': d10,
    '12': d12,
    '20': d20,
    '%': d00,
    '100': d00
}

DICE_ROLL_REGEX = r"(?P<Times>\d*)d(?P<Dice>4|6|8|10|12|20|%|100)"


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
        return int((self.score - 10) / 2)


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

    def __repr__(self):
        character_str: str = ''
        character_str += f'Name: {self.name}\n'
        character_str += f'Level: {self.level}\n'
        character_str += f'Stats: {'\t\n'.join([f'{stat}: {s.score}' for stat, s in self._stats.items()])}'
        return character_str

class Dnd5e(RolePlayingSystem):
    EXP = 'EXPERTISE'

    def check(self, character: Dnd5ECharacterSheet, skill: str, check_str: str = None) -> int:
        score = character.skill_score(skill)
        roll_result = roll_die(d20) + score
        check_mod: Dnd5eCheckMod = Dnd5eCheckMod.NONE
        if check_str:
            check_mod: Dnd5eCheckMod = CHECK_MODS.get(check_str, Dnd5eCheckMod.NONE)
        if check_mod == Dnd5eCheckMod.NONE:
            return roll_result
        alt_roll = roll_die(d20) + score
        if check_mod == Dnd5eCheckMod.ADVANTAGE:
            return max(roll_result, alt_roll)
        elif check_mod == Dnd5eCheckMod.DISADVANTAGE:
            return min(roll_result, alt_roll)
        else:
            raise ValueError(f'Got unknown Dnd5eCheckMod: {check_mod}')

    @staticmethod
    def roll(desc: str) -> int:
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

    def character_sheet(self, args_list: list[str]) -> Dnd5ECharacterSheet:
        name = args_list.pop(0)
        level = int(args_list.pop(0))
        stats = [int(stat) for stat in args_list[0:len(STATS)]]
        proficiencies = [prof for prof in args_list[len(STATS): args_list.index(self.EXP) if self.EXP in args_list else len(args_list)]]
        expertise = None
        if self.EXP in args_list:
            expertise = args_list[args_list.index(self.EXP)+1:]
        return Dnd5ECharacterSheet(name, level, stats, proficiencies, expertise)

    def __str__(self) -> str:
        return 'Dungeons and Dragons 5th Edition'
