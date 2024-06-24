from abc import ABC, abstractmethod

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class Repository[T: DeclarativeBase](ABC):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session: async_sessionmaker[AsyncSession] = session

    @abstractmethod
    async def get(self, _id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, _id: int, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, _id: int) -> T:
        raise NotImplementedError
