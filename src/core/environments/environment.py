from enum import Enum

from pydantic import BaseModel, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class EnvironmentTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class FastAPIKwargs(BaseModel):
    debug: bool
    docs_url: str
    openapi_prefix: str
    openapi_url: str
    redoc_url: str
    title: str
    version: str


class LoggingSettings(BaseModel):
    file: str
    rotation: str
    compression: str


class DatabaseSettings(BaseModel):
    url: PostgresDsn
    test_url: PostgresDsn


class AuthSettings(BaseModel):
    secret: SecretStr


class MiddlewareSettings(BaseModel):
    allow_origins: list[str]
    allow_credentials: bool
    allow_methods: list[str]
    allow_headers: list[str]


class Environment(BaseSettings):
    env_type: EnvironmentTypes
    fastapi_kwargs: FastAPIKwargs
    logging: LoggingSettings
    database: DatabaseSettings
    auth: AuthSettings
    middleware: MiddlewareSettings

    api_prefix: str
