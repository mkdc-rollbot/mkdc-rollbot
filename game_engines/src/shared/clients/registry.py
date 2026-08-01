from src.shared.clients.base_client import BaseClient
from src.shared.models import EngineRegistrationPayload


class RegistryClient(BaseClient):
    async def register(self, registration: EngineRegistrationPayload):
        return await self.post(
            "/registry/register",
            registration.model_dump()
        )

    async def heartbeat(self, engine_id: str):
        return await self.post("/registry/heartbeat", {"engine_id": engine_id})


    async def deregister(self, engine_id: str):
        return await self.post("/registry/deregister", { "engine_id": engine_id})
