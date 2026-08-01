from pydantic import BaseModel

class EnginePayload(BaseModel):
    ruleset: str
    url: str
