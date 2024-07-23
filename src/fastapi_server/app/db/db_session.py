from functools import lru_cache

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def get_async_engine() -> AsyncEngine | None:
    try:
        async_engine: AsyncEngine = create_async_engine(
            get_app_settings().database_url,
            future=True,
        )
        return async_engine
    except SQLAlchemyError as e:
        logger.warning("Unable to establish db engine, database might not exist yet")
        logger.warning(e)


async def initialize_database() -> None:
    async_engine = get_async_engine()
    async with async_engine.begin() as async_conn:
        await async_conn.run_sync(Table.metadata.create_all)

        logger.success("Initializing database was successfully.")
