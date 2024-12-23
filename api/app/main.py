import time

from fastapi import FastAPI, APIRouter, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.schemas.health import HealthResponse
from contextlib import asynccontextmanager
from app.core.db.engine import init_db, async_engine
from core.logging.logger import logger
from api.routers.users import router as users_router
from api.errors import (
    http_exception_handler,
    method_not_allowed_handler,
    not_found_handler,
    validation_exception_handler,
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
        logger.warning(f"{settings.env} server has stopped")


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
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint for Reverse proxy / Load balancer
@app.get("/health", response_model=HealthResponse, tags=["status"])
async def health_check_handler() -> HealthResponse:
    return HealthResponse(
        timestamp=time.time_ns(),
    )


router = APIRouter(prefix=f"/{settings.version}")
router.include_router(users_router)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.http_port)
