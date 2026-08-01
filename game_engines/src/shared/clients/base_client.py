from httpx import AsyncClient


class BaseClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.client = AsyncClient(
            timeout=timeout
        )

    async def close(self):
        await self.client.aclose()

    async def get(self, path: str):
        response = await self.client.get(
            f"{self.base_url}{path}"
        )
        response.raise_for_status()
        return response.json()

    async def post(
        self,
        path: str,
        payload: dict
    ):
        response = await self.client.post(
            f"{self.base_url}{path}",
            json=payload
        )
        response.raise_for_status()
        return response.json()
