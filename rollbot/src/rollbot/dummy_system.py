import json

from src.rollbot.system_base import CharacterSheet, RolePlayingSystem

class DummyCharacterSheet(CharacterSheet):
    def __init__(self, name):
        self.name = name

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
