from fastapi import FastAPI
from config import settings
from api.schemas.health.response import HealthResponse, SystemInfos
import time
from contextlib import asynccontextmanager
from core.db.engine import init_db, async_engine
from core.logging.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"starting {settings.env} server on :{settings.http_port}")
    try:
        await init_db()
        yield
    finally:
        await async_engine.dispose()
        logger.warning("server has stopped")


app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan,
)


# Health check endpoint for Reverse proxy / Load balancer
@app.get("/health", response_model=HealthResponse, tags=["status"])
async def health_check_handler() -> HealthResponse:
    return HealthResponse(
        timestamp=time.time_ns(),
        system_info=SystemInfos(env=settings.env, version=settings.version),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.http_port)
