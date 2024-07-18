from pydantic import BaseModel

from src.db.repositories.repository import Repository


class TasksRepository(Repository):
    async def create(self, **kwargs) -> BaseModel:
        pass

    async def get(self, **kwargs) -> BaseModel:
        pass

    async def update(self, **kwargs) -> BaseModel:
        pass

    async def delete(self, **kwargs) -> BaseModel:
        pass
