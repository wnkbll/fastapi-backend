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


class TestFastAPIKwargs(FastAPIKwargs):
    debug: bool = True
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Test FastAPI pet project"
    version: str = "0.0.0"


class TestLoggingSettings(LoggingSettings):
    file: str = "backend.log"
    rotation: str = "2MB"
    compression: str = "zip"


class TestPostgresSettings(PostgresSettings):
    url: PostgresDsn = env_values["DATABASE_URL"]
    test_url: PostgresDsn = env_values["TEST_DATABASE_URL"]


class TestRedisSettings(RedisSettings):
    url: RedisDsn = env_values["REDIS_URL"]
    test_url: RedisDsn = env_values["TEST_REDIS_URL"]


class TestAuthSettings(AuthSettings):
    secret: SecretStr = env_values["SECRET_KEY"]


class TestMiddlewareSettings(MiddlewareSettings):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class TestEnvironment(Environment):
    env_type: EnvironmentTypes = EnvironmentTypes.test
    fastapi_kwargs: FastAPIKwargs = TestFastAPIKwargs()
    logging: LoggingSettings = TestLoggingSettings()
    postgres: PostgresSettings = TestPostgresSettings()
    auth: AuthSettings = TestAuthSettings()
    middleware: MiddlewareSettings = TestMiddlewareSettings()

    api_prefix: str = "/api"
