from fastapi import FastAPI

from src.system_base import RolePlayingSystem, CharacterVariant

from .character_sheet import Dnd5ECharacterSheet
from .constants import Ability, Skill, ProficiencyLevel, CHECK_MODS, SKILLS_TO_ABILITIES
from .models import CharacterSheetPayload

class Dnd5e(RolePlayingSystem):
    def create_character(self, character: CharacterSheetPayload) -> Dnd5ECharacterSheet:
        return Dnd5ECharacterSheet(character)

    def register_routes(self, app: FastAPI):
        @app.post('/character/create')
        async def create_character(character: CharacterSheetPayload):
            try:
                self.create_character(character)
                return {"status": 200}
            except Exception:
                return {"status": 500}

        return app

    def __str__(self) -> str:
        return 'Dungeons and Dragons 5th Edition (2014)'

    def key(self):
        return 'dnd5e'

    def metadata(self):
        return {'key': self.key(),
                'name': str(self),
                'commands': [
                        {'id': 'character.create',
                         'endpoint': '/character/create'}
                    ]
                }
