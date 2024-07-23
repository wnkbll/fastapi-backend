from dotenv import dotenv_values
from pydantic import PostgresDsn, SecretStr, RedisDsn

from depricated.src.core import (
    FastAPIKwargs,
    LoggingSettings,
    PostgresSettings,
    RedisSettings,
    AuthSettings,
    MiddlewareSettings,
    Environment,
    EnvironmentTypes,
)
from depricated.src.core import ENV_PATH

env_values = dotenv_values(ENV_PATH)


class DevFastAPIKwargs(FastAPIKwargs):
    debug: bool = True
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Dev FastAPI pet project"
    version: str = "0.0.0"


class DevLoggingSettings(LoggingSettings):
    file: str = "backend.log"
    rotation: str = "2MB"
    compression: str = "zip"


class DevPostgresSettings(PostgresSettings):
    url: PostgresDsn = env_values["DATABASE_URL"]
    test_url: PostgresDsn = env_values["TEST_DATABASE_URL"]


class DevRedisSettings(RedisSettings):
    url: RedisDsn = env_values["REDIS_URL"]
    test_url: RedisDsn = env_values["TEST_REDIS_URL"]


class DevAuthSettings(AuthSettings):
    secret: SecretStr = env_values["SECRET_KEY"]


class DevMiddlewareSettings(MiddlewareSettings):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class DevelopmentEnvironment(Environment):
    env_type: EnvironmentTypes = EnvironmentTypes.dev
    fastapi_kwargs: FastAPIKwargs = DevFastAPIKwargs()
    logging: LoggingSettings = DevLoggingSettings()
    postgres: PostgresSettings = DevPostgresSettings()
    redis: RedisSettings = DevRedisSettings()
    auth: AuthSettings = DevAuthSettings()
    middleware: MiddlewareSettings = DevMiddlewareSettings()

    api_prefix: str = "/api"
