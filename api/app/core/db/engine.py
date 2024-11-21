from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from config import settings

async_engine = create_async_engine(
    url=settings.database_url,
    echo=True,
    poolclass=AsyncAdaptedQueuePool,
)
