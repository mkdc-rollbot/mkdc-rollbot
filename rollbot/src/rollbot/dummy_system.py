import json

from src.rollbot.system_base import CharacterSheet, RolePlayingSystem, CharacterVariant

from typing import Any

class DummyVariant(CharacterVariant):
    def validate_diffs(self, diffs: dict[str, Any]):
        return True

    def parse_diffs(self, diffs: dict[str, Any]):
        return diffs

class DummyCharacterSheet(CharacterSheet):
    def __init__(self, name):
        self.name = name


    @classmethod
    def fromJson(cls, json: dict[str: Any]):
        return cls(**json)

    def apply_diff(self, variant: DummyVariant):
        for key, val in variant.__dict__:
            self.__dict__[key] = val

    def toJson(self):
        return self.__dict__

class DummySystem(RolePlayingSystem):
    def character_sheet(self, args_list: list[str]) -> (DummyCharacterSheet, str):
        name = ' '.join(args_list)
        sheet = DummyCharacterSheet(name)
        return sheet, name

    def parse(self, *args):
        return 'That sure was a thing to parse!'

    def __str__(self) -> str:
        return 'Dummy system for debug purposes'

    def key(self):
        return 'dummy'
