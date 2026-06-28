from pydantic import BaseModel
from typing import Any


class ChannelPayload(BaseModel):
    guild_id: int
    channel_id: int


class ChannelSettingsPayload(BaseModel):
    channel_id: int
    prefix: str | None
    system: str | None


class CharacterPayload(BaseModel):
    author_id: int
    name: str
    character_sheet: dict
    channel_id: int
