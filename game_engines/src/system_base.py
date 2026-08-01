from abc import ABC, abstractmethod
from fastapi import FastAPI
from typing import Any


class CharacterVariant(ABC):
    """
    This class encapsulates changes to a character sheet to be applied
    """
    def __init__(self, diffs: dict[str: Any]):
        self.validate_diffs(diffs)
        self._diffs = self.parse_diffs(diffs)

    @classmethod
    def from_json(cls, json: str):
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
    def to_json(self):
        ...

    @staticmethod
    @abstractmethod
    def from_json(json: str):
        ...

    @abstractmethod
    def apply_diff(variant: CharacterVariant):
        ...

class RolePlayingSystem(ABC):
    """
    This class encapsulates role-playing systems: Character sheets structure and Check handling.
    """
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def register_routes(self, app: FastAPI) -> FastAPI:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    def key(self) -> str:
        ...

    @abstractmethod
    def metadata(self) -> dict:
        ...
