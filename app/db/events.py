from sqlalchemy.ext.asyncio import AsyncEngine

from app.models.orm.common import Model


async def init_models(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
