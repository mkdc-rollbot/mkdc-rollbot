from src.shared.clients.base_client import BaseClient
from rollbot_sdk.models.dice import DiceRequest


class DiceClient(BaseClient):
    async def roll(self, notation: str):
        request = DiceRequest(notation=notation)

        return await self.post("/roll", request.model_dump())
