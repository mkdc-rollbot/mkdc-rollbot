from fastapi import FastAPI
from types import MappingProxyType
from typing import Mapping

from src.system_base import RolePlayingSystem, CharacterVariant

from .character_sheet import Dnd5ECharacterSheet
from .constants import Ability, Skill, ProficiencyLevel, Dnd5eCheckMod, CHECK_MODS, SKILLS_TO_ABILITIES
from .models import CharacterSheetPayload

class Dnd5e(RolePlayingSystem):
    CHECK_ROLLS: Mapping[Dnd5eCheckMod, str] = MappingProxyType({
        Dnd5eCheckMod.NONE: '1d20',
        Dnd5eCheckMod.ADVANTAGE: '2d20kh1',
        Dnd5eCheckMod.DISADVANTAGE: '2d20kl1'
        })

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

        @app.get('/roll/{notation}')
        async def roll(notation: str):
            return await self.roll(notation)

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

    async def roll(self, notation: str):
        if not self.dice_client:
            raise Exception('No dice client set yet')
        
        response = await self.dice_client.roll(notation)
        return response

    async def roll_check(self, mod: str | None = None):
        if mod and mod not in CHECK_MODS:
            raise ValueError(f'Invalid check mod {mod}')

        mod = '' if not mod else mod
        mod = CHECK_MODS.get(mod, Dnd5eCheckMod.NONE)
        notation = self.CHECK_ROLLS[mod]

        return await self.roll(notation)
