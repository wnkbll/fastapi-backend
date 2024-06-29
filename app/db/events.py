from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncEngine

from app.db.connection import DatabaseConnection
from app.models.tables import Table


@lru_cache
def get_db_connection() -> DatabaseConnection:
    db_connection = DatabaseConnection()
    return db_connection


async def init_models(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Table.metadata.create_all)
