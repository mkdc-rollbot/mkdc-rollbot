from pydantic import BaseModel

class EngineRegistrationPayload(BaseModel):
    ruleset: str
    url: str
