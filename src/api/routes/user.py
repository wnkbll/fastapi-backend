from fastapi import APIRouter, Depends, Body, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from src.api.dependencies.authentication import get_current_user_authorizer
from src.core.environments import Environment
from src.core.settings import get_app_settings
from src.db.connection import DatabaseConnection
from src.db.events import get_db_connection
from src.db.repositories.users import UsersRepository
from src.models.schemas.users import User, UserInResponse, UserWithToken, UserInUpdate, UserInDB
from src.resources import strings
from src.services import jwt
from src.services.authentication import check_email_is_taken, check_username_is_taken

router = APIRouter()


@router.get("", response_model=UserInResponse, name="user:get-current-user")
async def get_current_user(
        user: User = Depends(get_current_user_authorizer()),
        settings: Environment = Depends(get_app_settings)
) -> UserInResponse:
    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value())
    )

    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token
        )
    )


@router.put("", response_model=UserInResponse, name="user:update-current-user")
async def update_current_user(
        user_update: UserInUpdate = Body(..., embed=True, alias="user"),
        current_user: UserInDB = Depends(get_current_user_authorizer()),
        db_connection: DatabaseConnection = Depends(get_db_connection),
        settings: Environment = Depends(get_app_settings),
) -> UserInResponse:
    users_repo: UsersRepository = UsersRepository(db_connection.session_factory)

    if user_update.username and user_update.username != current_user.username:
        if await check_username_is_taken(users_repo, user_update.username):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=strings.USERNAME_TAKEN,
            )

    if user_update.email and user_update.email != current_user.email:
        if await check_email_is_taken(users_repo, user_update.email):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=strings.EMAIL_TAKEN,
            )

    user = await users_repo.update_user(user=current_user, **user_update.model_dump())

    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token,
        ),
    )
