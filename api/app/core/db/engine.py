from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from config import settings
from app.core.logging.logger import logger

async_engine = AsyncEngine(
    create_engine(
        url=settings.database_url,
        echo=True,
        pool_size=20,
        max_overflow=5,
    )
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(lambda _: logger.info("Database initialized"))
