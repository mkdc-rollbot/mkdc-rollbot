from constants import Ability, Skill, SkillModifier, CHECK_MODS, SKILLS_TO_ABILITIES
from .system_base import CharacterSheet, RolePlayingSystem, CharacterVariant

class Dnd5e(RolePlayingSystem):
    EXP = 'EXPERTISE'

    def check(self, character: Dnd5ECharacterSheet, skill: str, check_str: str = None) -> int:
        ...

    def character_sheet(self, args_list: list[str]) -> (Dnd5ECharacterSheet, str):
        name = args_list.pop(0)
        level = int(args_list.pop(0))
        abilities = [int(ability) for abilitie in args_list[0:len(Ability)]]
        proficiencies = [prof for prof in args_list[len(Ability): args_list.index(self.EXP) if self.EXP in args_list else len(args_list)]]
        expertise = None
        if self.EXP in args_list:
            expertise = args_list[args_list.index(self.EXP)+1:]
        return Dnd5ECharacterSheet(name, level, abilities, proficiencies, expertise), name

    def __str__(self) -> str:
        return 'Dungeons and Dragons 5th Edition (2014)'

    def key(self):
        return 'dnd5e'
