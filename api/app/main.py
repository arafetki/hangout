import time

from fastapi import FastAPI, APIRouter, status, HTTPException
from fastapi.exceptions import RequestValidationError
from config import settings
from api.schemas.health import HealthResponse, SystemInfos
from contextlib import asynccontextmanager
from core.db.engine import init_db, async_engine
from core.logging.logger import logger
from api.routers.users import router as users_router
from api.errors import (
    http_exception_handler,
    method_not_allowed_handler,
    not_found_handler,
    validation_execption_handler,
    unhandled_exception_handler,
)


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

app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_handler)
app.add_exception_handler(status.HTTP_405_METHOD_NOT_ALLOWED, method_not_allowed_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_execption_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


# Health check endpoint for Reverse proxy / Load balancer
@app.get("/health", response_model=HealthResponse, tags=["status"])
async def health_check_handler() -> HealthResponse:
    return HealthResponse(
        timestamp=time.time_ns(),
        system_info=SystemInfos(env=settings.env, version=settings.version),
    )


router = APIRouter(prefix=f"/{settings.version}", tags=["v1"])
router.include_router(users_router)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.http_port)
