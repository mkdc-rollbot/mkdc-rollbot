from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    database_url: str
    log_level: str
    api_port: int

settings = Settings(
    database_url=os.environ["DATABASE_URL"],
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    api_port=int(os.getenv("API_PORT", "11037")),
)
