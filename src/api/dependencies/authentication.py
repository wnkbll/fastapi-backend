from typing import Callable, Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.environments import Environment
from src.core.settings import get_app_settings
from src.db.connection import DatabaseConnection
from src.db.errors import EntityDoesNotExistError
from src.db.events import get_db_connection
from src.db.repositories.users import UsersRepository
from src.models.schemas.users import UserInDB
from src.resources import strings
from src.services import jwt

HEADER_KEY = "Authorization"


class AppAPIKeyHeader(APIKeyHeader):
    async def __call__(
            self,
            request: requests.Request,
    ) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail=strings.AUTHENTICATION_REQUIRED,
            )


def get_current_user_authorizer(*, required: bool = True) -> Callable:
    return _get_current_user if required else _get_current_user_optional


def _get_authorization_header_retriever(
        *,
        required: bool = True,
) -> Callable:  # type: ignore
    return _get_authorization_header if required else _get_authorization_header_optional


def _get_authorization_header(
        api_key: str = Security(AppAPIKeyHeader(name=HEADER_KEY)),
        settings: Environment = Depends(get_app_settings),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )
    if token_prefix != settings.jwt_token_prefix:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )

    return token


def _get_authorization_header_optional(
        authorization: Optional[str] = Security(
            AppAPIKeyHeader(name=HEADER_KEY, auto_error=False),
        ),
        settings: Environment = Depends(get_app_settings),
) -> str:
    if authorization:
        return _get_authorization_header(authorization, settings)

    return ""


async def _get_current_user(
        db_connection: DatabaseConnection = Depends(get_db_connection),
        token: str = Depends(_get_authorization_header_retriever()),
        settings: Environment = Depends(get_app_settings),
) -> UserInDB:
    repo: UsersRepository = UsersRepository(db_connection.session_factory)

    try:
        username = jwt.get_username_from_token(
            token,
            str(settings.secret_key.get_secret_value()),
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )

    try:
        return await repo.get_user_by_username(username=username)
    except EntityDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )


async def _get_current_user_optional(
        db_connection: DatabaseConnection = Depends(get_db_connection),
        token: str = Depends(_get_authorization_header_retriever(required=False)),
        settings: Environment = Depends(get_app_settings),
) -> Optional[UserInDB]:
    if token:
        return await _get_current_user(db_connection, token, settings)

    return None
