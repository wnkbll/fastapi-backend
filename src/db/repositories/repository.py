from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class Repository:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory: async_sessionmaker[AsyncSession] = session_factory

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    async def create(self, **kwargs) -> BaseModel:
        raise NotImplementedError

    async def get(self, **kwargs) -> BaseModel:
        raise NotImplementedError

    async def get_all(self, **kwargs) -> list[BaseModel]:
        raise NotImplementedError

    async def update(self, **kwargs) -> BaseModel:
        raise NotImplementedError

    async def delete(self, **kwargs) -> BaseModel:
        raise NotImplementedError
