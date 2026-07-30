from abc import ABC, abstractmethod
from typing import Any


class CharacterVariant(ABC):
    """
    This class encapsulates changes to a character sheet to be applied
    """
    def __init__(self, diffs: dict[str: Any]):
        self.validate_diffs(diffs)
        self._diffs = self.parse_diffs(diffs)

    @classmethod
    def fromJson(cls, json: str):
        return cls(json)

    @abstractmethod
    def validate_diffs(self, diffs: dict[str, Any]):
        ...

    @abstractmethod
    def parse_diffs(self, diffs: dict[str, Any]):
        ...
        
    def __contains__(self, key):
        return key in self._diffs.keys()

    def __getitem__(self, key):
        return self._diffs[key]

class CharacterSheet(ABC):
    """
    This class encapsulates character sheets.
    """
    @abstractmethod
    def toJson(self):
        ...

    @staticmethod
    @abstractmethod
    def fromJson(json: str):
        ...

    @abstractmethod
    def apply_diff(variant: CharacterVariant):
        ...

class RolePlayingSystem(ABC):
    """
    This class encapsulates role-playing systems: Character sheets structure and Check handling.
    """
    @abstractmethod
    def character_sheet(self, args_list: list[str]) -> (CharacterSheet, str):
        ...

    @abstractmethod
    def parse(self, *args):
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    def key(self) ->str:
        ...
