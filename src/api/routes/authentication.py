from fastapi import APIRouter, Body

from src.api.dependencies import UsersRepositoryDepends
from src.models.schemas.users import UserInResponse, UserInLogin, UserInCreate

router = APIRouter()


@router.post("", name="auth:login", response_model=UserInResponse)
async def login(
        user_repo: UsersRepositoryDepends,
        user_in_login: UserInLogin = Body(),
) -> UserInResponse:
    pass


@router.post("", name="auth:register", response_model=UserInResponse)
async def register(
        user_repo: UsersRepositoryDepends,
        user_in_create: UserInCreate = Body(alias="user-in-create"),
) -> UserInResponse:
    pass
