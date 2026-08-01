from enum import Enum, Flag, auto
from typing import Mapping
from types import MappingProxyType

############################################
# CONSTANTS
############################################

class ProficiencyLevel(Flag):
    PROFICIENCY = auto()
    EXPERTISE = auto()

class Dnd5eCheckMod(Enum):
    NONE = 0
    ADVANTAGE = 1
    DISADVANTAGE = 2

CHECK_MODS: Mapping[str, Dnd5eCheckMod] = MappingProxyType({
    'advantage': Dnd5eCheckMod.ADVANTAGE,
    'disadvantage': Dnd5eCheckMod.DISADVANTAGE
})

class Ability(Enum):
    STR = 'str'
    DEX = 'dex'
    CON = 'con'
    INT = 'int'
    WIS = 'wis'
    CHA = 'cha'

    @classmethod
    def from_str(cls, value: str) -> "Ability":
        return cls(value)

class Skill(Enum):
    ACROBATICS = 'acrobatics'
    ANIMAL_HANDLING = 'animal handling'
    ARCANA = 'arcana'
    ATHLETICS = 'athletics'
    DECEPTION = 'deception'
    HISTORY = 'history'
    INSIGHT = 'insight'
    INTIMIDATION = 'intimidation'
    INVESTIGATION = 'investigation'
    MEDICINE = 'medicine'
    NATURE = 'nature'
    PERCEPTION = 'perception'
    PERFORMANCE = 'performance'
    PERSUASION = 'persuasion'
    RELIGION = 'religion' 
    SLEIGHT_OF_HAND = 'sleight of hand' 
    STEALTH = 'stealth'
    SURVIVAL = 'survival'

    @classmethod
    def from_str(cls, value: str) -> "Skill":
        return cls(value)

SKILLS_TO_ABILITIES: Mapping[Skill, Ability] = MappingProxyType({
    Skill.ACROBATICS: Ability.DEX,
    Skill.ANIMAL_HANDLING: Ability.WIS,
    Skill.ARCANA: Ability.INT,
    Skill.ATHLETICS: Ability.STR,
    Skill.DECEPTION: Ability.CHA,
    Skill.HISTORY: Ability.INT,
    Skill.INSIGHT: Ability.WIS,
    Skill.INTIMIDATION: Ability.CHA,
    Skill.INVESTIGATION: Ability.INT,
    Skill.MEDICINE: Ability.WIS,
    Skill.NATURE: Ability.INT,
    Skill.PERCEPTION: Ability.WIS,
    Skill.PERFORMANCE: Ability.CHA,
    Skill.PERSUASION: Ability.CHA,
    Skill.RELIGION: Ability.INT,
    Skill.SLEIGHT_OF_HAND: Ability.DEX,
    Skill.STEALTH: Ability.DEX,
    Skill.SURVIVAL: Ability.WIS
})

# =======================
# CHARACTER SHEET SCHEMA
# =======================

SCHEMA = {
    'name': str,
    'level': int,
    'stats': {ability: int for ability in Ability},
    'skills': {skill: int for skill in Skill},
}
