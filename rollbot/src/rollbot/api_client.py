import requests

from typing import Final

PORT: Final = 11037
API_URL: Final = f'http://127.0.0.1:{PORT}'

class APIClient:
    def __init__(self):
        ...

    async def validate_guild_and_channel(self, guild_id, channel_id):
        response = await requests.post(f'{API_URL}/channel/', json={'guild_id': guild_id, 'channel_id': channel_id})
        return repsonse

    async def create_character(self, author_id, name, character_sheet, channel_id):
        response = await requests.post(f'{API_URL}/character/', json={'author_id': author_id, 'name': name, 'character_sheet': character_sheet, 'channel_id': channel_id})
        return response.character_id
