from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.db.repositories import UsersRepository
from app.db import get_db_engine, get_db_session

router = APIRouter()

engine: AsyncEngine = get_db_engine()
session: async_sessionmaker[AsyncSession] = get_db_session(engine)
user_repository: UsersRepository = UsersRepository(session)


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await user_repository.get(user_id)
    return {"id": user.id, "name": user.name, "age": user.age, "passport": user.passport}
