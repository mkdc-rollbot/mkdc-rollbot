from pydantic import BaseModel
from typing import Any


class ChannelPayload(BaseModel):
    guild_id: str
    channel_id: str


class ChannelSettingsPayload(BaseModel):
    channel_id: str
    prefix: str | None
    system: str | None

class CharacterPayload(BaseModel):
    author_id: str
    name: str
    character_sheet: dict[str, Any]
    channel_id: str
