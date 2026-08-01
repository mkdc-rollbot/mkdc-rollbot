from pydantic import BaseModel

class CharacterSheetPayload(BaseModel):
    name: str
    level: int
    abilities: dict[str, int]
    skills_proficiencies: list[str]
    skills_expertise: list[str]
