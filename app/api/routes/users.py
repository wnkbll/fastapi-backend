from fastapi import APIRouter, Depends

from app.db.repositories.users import UsersRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.get("/users/{user_id}")
async def get_user(user_id: int, user_repository: UsersRepository = Depends(get_repository(UsersRepository))):
    user = await user_repository.get(user_id)
    return user
