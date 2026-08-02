from src.shared.clients.base_client import BaseClient


class DiceClient(BaseClient):
    async def roll(self, notation: str):
        return await self.post(f"/roll/{notation}")
