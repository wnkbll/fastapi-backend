from fastapi import APIRouter
from src.models.schemas.users import UserInResponse
from src.api.dependencies import UsersRepositoryDepends

router = APIRouter()


@router.post("", name="auth:login", response_model=UserInResponse)
async def login(
        user_repo: UsersRepositoryDepends
) -> UserInResponse:
    pass
