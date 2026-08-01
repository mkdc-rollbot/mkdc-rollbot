from typing import Any

from src.system_base import CharacterSheet

from .constants import Ability, Skill, ProficiencyLevel, CHECK_MODS, SKILLS_TO_ABILITIES
from .variants import Dnd5ECharacterVariant
from .models import CharacterSheetPayload

############################################
# UTILITY CLASSES
############################################

class CharacterAbility:
    def __init__(self, score: int):
        self.score = score

    @property
    def modifier(self) -> int:
        return int((self.score - 10) // 2)


class CharacterSkill:
    def __init__(self, ability: CharacterAbility, proficiency: ProficiencyLevel):
        self.ability = ability
        self.proficiency = proficiency

    def score(self, prof_bonus: int) -> int:
        prof_multiplier = 0
        if ProficiencyLevel.PROFICIENCY in self.proficiency:
            prof_multiplier += 1
            if ProficiencyLevel.EXPERTISE in self.proficiency:
                prof_multiplier += 1
        return self.ability.modifier + (prof_bonus * prof_multiplier)


class Dnd5ECharacterSheet(CharacterSheet):
    def __init__(self, character: CharacterSheetPayload):
        Dnd5ECharacterSheet.validate(character)

        self.name: str = character.name
        self.level: int = character.level

        ability_scores = character.abilities
        self.abilities = {ability: CharacterAbility(score) for ability, score in ability_scores.items()}

        proficiency_levels: dict[Skill, ProficiencyLevel] = {skill: ProficiencyLevel(0) for skill in Skill}
        for skill in skill_proficiencies:
            proficiency_levels[skill] |= ProficiencyLevel.PROFICIENCY
        if expertise:
            for skill in expertise:
                proficiency_levels[skill] |= ProficiencyLevel.EXPERTISE
        self._skills = {skill: CharacterSkill(self.abilities[ability], proficiency_levels[skill]) for skill, ability in SKILLS_TO_ABILITIES.items()}

        self.saving_throws_proficiencies = {ability: CharacterSkill(ability, ProficiencyLevel.PROFICIENCY) if ability in character.saving_throws_proficiencies else CharacterSkill(ability, ProficiencyLevel(0)) for ability in Ability}

    @staticmethod
    def validate_data(character: CharacterSheetPayload):
        level = character.level
        if not 1 <= level <= 20:
            raise ValueError(f'Invalid level {level}')

        ability_scores = character.abilities
        if len(ability_scores) != len(Ability) or not all([1 <= ability <= 20 for ability in ability_scores]):
            raise ValueError(f'Invalid ability scroes given.')

        skill_proficiencies = character.skill_proficiencies
        expertise = character.skill_expertise
        if any([skill not in skill_proficiencies for skill in expertise]):
            raise ValueError('All expertise skills require proficiency.')

    @property
    def proficiency_modifier(self):
        return 2 + (self.level - 1) // 4

    def skill_score(self, skill):
        assert skill in Skill 
        return self._skills[skill].score(self.proficiency_modifier)

    @classmethod
    def from_json(cls, json: dict[str, Any]):
        name = json['name']
        level = json['level']
        abilities = [json["abilities"][ability.value] for ability in Ability]
        skills = {}
        for skill in json['skills']:
            skills[skill] =int(json['skills'][skill])
        skill_proficiencies = [skill for skill, mod in skills.items() if mod & ProficiencyLevel.PROFICIENCY.value]
        expertise = [skill for skill, mod in skills.items() if mod & ProficiencyLevel.EXPERTISE.value]
        return cls(name, level, abilities, skill_proficiencies, expertise)

    def apply_diff(self, variant: Dnd5ECharacterVariant):
        if 'name' in variant:
            self.name = variant['name']
        if 'level' in variant:
            self.level = variant['level']
        if 'abilities' in variant:
            for ability in variant['abilities']:
                self.abilities[ability] = CharacterAbility(variant['abilities'][ability])
        if 'skills' in variant:
            for skill in variant['skills']:
                self._skills[skill].proficiency = ProficiencyLevel(int(variant['skills'][skill]))

    def __repr__(self):
        character_str: str = ''
        character_str += f'Name: {self.name}\n'
        character_str += f'Level: {self.level}\n'
        character_str += f'Abilities: {'\t\n'.join([f'{ability}: {a.score}' for ability, a in self.abilities.items()])}'
        return character_str

    def to_json(self):
        json = {'name': self.name,
                'level': self.level,
                'abilities': {name: ability.value for name, ability in self.abilities.items()},
                'skills': {name: skill.proficiency.value for name, skill in self._skills.items()},
                'saving_throws': self.saving_throws_proficiencies
                }
        return json


