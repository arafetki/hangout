from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    project_name: str
    project_description: str
    version: str = "0.1.0"
    env: Literal["development", "staging", "production"] = "development"
    http_port: int = 8080
    debug: bool = True
    database_url: str
    database_url_sync: str


settings = Settings()
