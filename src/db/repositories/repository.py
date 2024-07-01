from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class Repository(ABC):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory: async_sessionmaker[AsyncSession] = session_factory

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory
