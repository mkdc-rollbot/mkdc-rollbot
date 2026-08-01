from pydantic import BaseModel

from .constants import Ability, Skill

class CharacterSheetPayload(BaseModel):
    name: str
    level: int
    abilities: dict[Ability, int]
    saving_throws_proficiencies: list[Ability]
    skills_proficiencies: list[Skill]
    skills_expertise: list[Skill]
