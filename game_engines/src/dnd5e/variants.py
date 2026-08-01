from typing import Any

from src.system_base import CharacterVariant
from .constants import SCHEMA

class Dnd5ECharacterVariant(CharacterVariant):
    def validate_diffs(self, diffs: dict[str, Any]):
        if not diffs:
            raise ValueError('Empty diff')
        for key, value in diffs.items():
            split_key = key.split('.')
            schema = SCHEMA
            for current_key in split_key:
                if current_key not in schema.keys():
                    raise KeyError(f'Key {current_key} in {key} is not part of the schema.')
                schema = schema[current_key]
            if not isinstance(value, schema):
                raise ValueError(f'Value for {key} should be of type {schema}, got {type(value)}.')

    def parse_diffs(self, diffs: dict[str, Any]):
        parsed_diffs = {}
        for key, value in diffs.items():
            split_key = key.split('.')
            current_diffs = parsed_diffs
            for current_key in split_key[:-1]:
                if current_key not in current_diffs.keys():
                    current_diffs[current_key] = dict()
                current_diffs = current_diffs[current_key]
            current_diffs[current_key] = value
        return parsed_diffs


