from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    port: int = 8080
    env: Literal["development", "staging", "production"] = "development"
    version: str = "0.1.0"
    debug: bool = True
    database_url: str = "sqlite+aiosqlite://sqlite.db"


settings = Settings()
