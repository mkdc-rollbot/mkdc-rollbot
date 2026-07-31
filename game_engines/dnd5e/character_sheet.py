from typing import Any, Mapping

from .system_base import CharacterSheet

from constants import Ability, Skill, SkillModifier, CHECK_MODS, SKILLS_TO_ABILITIES

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
    def __init__(self, ability: CharacterAbility, modifier: SkillModifier):
        self.ability = ability
        self.modifier = modifier

    def score(self, prof_bonus: int) -> int:
        prof_multiplier = 0
        if SkillModifier.PROFICIENCY in self.modifier:
            prof_multiplier += 1
            if SkillModifier.EXPERTISE in self.modifier:
                prof_multiplier += 1
        return self.ability.modifier + (prof_bonus * prof_multiplier)



class Dnd5ECharacterSheet(CharacterSheet):
    def __init__(self, name: str, level: int, ability_scores: list[int], proficiencies: list[str], expertise: list[str] = None):
        assert len(ability_scores) == len(Ability) and all([1 <= ability <= 20 for ability in ability_scores])
        self._abilities = {ability: CharacterAbility(score) for ability, score in zip(Ability, ability_scores)}
        self.name: str = name
        self.level: int = level
        modifiers: Mapping[Skill, SkillModifier] = {skill: SkillModifier(0) for skill in Skills}
        for skill in proficiencies:
            modifiers[skill] |= SkillModifier.PROFICIENCY
        if expertise:
            for skill in expertise:
                assert skill in proficiencies
                modifiers[skill] |= SkillModifier.EXPERTISE
        self._skills = {skill: CharacterSkill(self._abilities[ability], modifiers[skill]) for skill, ability in SKILLS_TO_ABILITIES.items()}

    @property
    def proficiency_modifier(self):
        return 2 + (self.level - 1) // 4

    def skill_score(self, skill):
        assert skill in Skills 
        return self._skills[skill].score(self.proficiency_modifier)

    @classmethod
    def from_json(cls, json: dict[str, Any]):
        name = json['name']
        level = json['level']
        abilities = []
        for ability in json['abilities']:
            abilities.append(json['abilities'][ability])
        skills = {}
        for skill in json['skills']:
            skills[skill] =int(json['skills'][skill])
        proficiencies = [skill for skill, mod in skills.items() if mod & SkillModifier.PROFICIENCY.value]
        expertise = [skill for skill, mod in skills.items() if mod & SkillModifier.EXPERTISE.value]
        return cls(name, level, abilities, proficiencies, expertise)

    def apply_diff(self, variant: Dnd5ECharacterVariant):
        if 'name' in variant:
            self.name = variant['name']
        if 'level' in variant:
            self.level = variant['level']
        if 'abilities' in variant:
            for ability in variant['abilities']:
                self._abilities[ability] = CharacterAbility(variant['abilities'][ability])
        if 'skills' in variant:
            for skill in variant['skills']:
                self._skills[skill].modifier = SkillModifier(int(variant['skills'][skill]))

    def __repr__(self):
        character_str: str = ''
        character_str += f'Name: {self.name}\n'
        character_str += f'Level: {self.level}\n'
        character_str += f'Abilities: {'\t\n'.join([f'{ability}: {a.score}' for ability, a in self._abilities.items()])}'
        return character_str

    def to_json(self):
        json = {'name': self.name,
                'level': self.level,
                'abilities': {name: ability.score for name, ability in self._abilities.items()},
                'skills': {name: skill.modifier.value for name, skill in self._skills.items()}
                }
        return json


