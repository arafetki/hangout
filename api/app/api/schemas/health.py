from typing import TypedDict, Literal
from pydantic import BaseModel


class SystemInfos(TypedDict):
    env: Literal["development", "staging", "production"]
    version: str


class HealthResponse(BaseModel):
    timestamp: int
    system_info: SystemInfos
