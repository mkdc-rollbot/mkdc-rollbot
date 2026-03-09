from abc import ABC, abstractmethod
from collections import namedtuple
from random import randint


Die = namedtuple('Die', ['min', 'max'])


def roll_die(die: Die) -> int:
    return randint(*die)


class CharacterSheet(ABC):
    """
    This class encapsulates character sheets.
    """
    ...


class RolePlayingSystem(ABC):
    """
    This class encapsulates role-playing systems: Character sheets structure and Check handling.
    """
    @abstractmethod
    def character_sheet(self, args_list: list[str]) -> CharacterSheet:
        ...

    @abstractmethod
    def check(self, *args):
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...
