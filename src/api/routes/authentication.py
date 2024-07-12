from fastapi import APIRouter, Body, HTTPException, status

from src.api.dependencies import UsersRepositoryDepends, SettingsDepends
from src.db.errors import EntityDoesNotExistError
from src.models.schemas.users import (
    UserInResponse, UserInLogin, UserInCreate, UserWithToken
)
from src.services import jwt, auth

router = APIRouter()


@router.post("/login", name="auth:login", response_model=UserInResponse)
async def login(
        settings: SettingsDepends,
        users_repo: UsersRepositoryDepends,
        user_in_login: UserInLogin = Body(),
) -> UserInResponse:
    try:
        user_in_db = await users_repo.get_user_by_email(email=user_in_login.email)
    except EntityDoesNotExistError as existence_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or email",
        ) from existence_error

    if not user_in_db.verify_password(user_in_login.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or email",
        )

    token = jwt.create_access_token_for_user(
        user_in_db, settings.auth.secret,
    )

    return UserInResponse(
        user=UserWithToken(
            username=user_in_db.username,
            email=user_in_db.email,
            bio=user_in_db.bio,
            image=user_in_db.image,
            token=token,
        ),
    )


@router.post("/register", name="auth:register", response_model=UserInResponse)
async def register(
        settings: SettingsDepends,
        users_repo: UsersRepositoryDepends,
        user_in_create: UserInCreate = Body(alias="user-in-create"),
) -> UserInResponse:
    if await auth.is_username_taken(users_repo, user_in_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken.",
        )

    if await auth.is_email_taken(users_repo, user_in_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already taken.",
        )

    user_in_db = await users_repo.create_user(user_in_create=user_in_create)

    token = jwt.create_access_token_for_user(
        user_in_db, settings.auth.secret,
    )

    return UserInResponse(
        user=UserWithToken(
            username=user_in_db.username,
            email=user_in_db.email,
            bio=user_in_db.bio,
            image=user_in_db.image,
            token=token,
        ),
    )
