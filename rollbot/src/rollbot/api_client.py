import httpx

from typing import Final

PORT: Final = 11037
API_URL: Final = f'http://127.0.0.1:{PORT}'

class APIClient:
    def __init__(self):
        ...

    async def validate_guild_and_channel(self, guild_id, channel_id):
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{API_URL}/channel/', json={'guild_id': str(guild_id), 'channel_id': str(channel_id)})
        return response.json()

    async def create_character(self, author_id, name, character_sheet, channel_id):
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{API_URL}/character/', json={'author_id': author_id, 'name': name, 'character_sheet': character_sheet, 'channel_id': channel_id})
        return response.character_id

    async def update_channel_settings(self, channel_id, prefix: str | None, system: str | None):
        async with httpx.AsyncClient() as client:
            response = await client.put(f'{API_URL}/channel/', json={'channel_id': channel_id, 'prefix': prefix, 'system': system})
        return response.json()

    async def get_characters_for_channel(self, channel_id):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{API_URL}/characters/', json={})
        return response.json()
