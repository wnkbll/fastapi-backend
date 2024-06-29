from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from app.core.environments import Environment
from app.core.settings import get_app_settings
from app.db.connection import DatabaseConnection
from app.db.errors import EntityDoesNotExistError
from app.db.events import get_db_connection
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import UserInResponse, UserInLogin, UserWithToken, UserInCreate, UserInDB
from app.resources import strings
from app.services import jwt
from app.services.authentication import check_email_is_taken, check_username_is_taken

router = APIRouter()


@router.post("/login", response_model=UserInResponse, name="auth:login")
async def login(
        user_login: UserInLogin = Body(..., embed=False, alias="user"),
        db_connection: DatabaseConnection = Depends(get_db_connection),
        settings: Environment = Depends(get_app_settings),
) -> UserInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=strings.INCORRECT_LOGIN_INPUT,
    )

    users_repo: UsersRepository = UsersRepository(db_connection.session_factory)

    try:
        user: UserInDB = await users_repo.get_user_by_email(email=user_login.email)
    except EntityDoesNotExistError as existence_error:
        raise wrong_login_error from existence_error

    if not user.check_password(user_login.password):
        raise wrong_login_error

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
            token=token,
        )
    )


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
    name="auth:register"
)
async def register(
        user_create: UserInCreate = Body(..., embed=False, alias="user"),
        db_connection: DatabaseConnection = Depends(get_db_connection),
        settings: Environment = Depends(get_app_settings),
) -> UserInResponse:
    users_repo: UsersRepository = UsersRepository(db_connection.session_factory)

    if await check_username_is_taken(users_repo, user_create.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN,
        )

    if not await check_email_is_taken(users_repo, user_create.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )

    user = await users_repo.create_user(**user_create.model_dump())

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
        )
    )
