from pydantic import BaseModel


class HealthResponse(BaseModel):
    timestamp: int
