import time
from api.schemas.health.response import HealthResponse, SystemInfos
from config import settings
from fastapi import FastAPI

app = FastAPI(debug=settings.debug, version=settings.version)


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["status"],
)
async def health_check() -> HealthResponse:
    return HealthResponse(
        timestamp=time.time_ns(),
        system_info=SystemInfos(env=settings.env, version=settings.version),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.port)
