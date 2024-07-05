from dotenv import dotenv_values
from pydantic import PostgresDsn, SecretStr

from src.core.environments.environment import (
    FastAPIKwargs,
    LoggingSettings,
    DatabaseSettings,
    AuthSettings,
    MiddlewareSettings,
    Environment,
    EnvironmentTypes,
)
from src.core.paths import ENV_PATH

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


class TestDatabaseSettings(DatabaseSettings):
    url: PostgresDsn = env_values["DATABASE_URL"]
    test_url: PostgresDsn = env_values["TEST_DATABASE_URL"]


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
    database: DatabaseSettings = TestDatabaseSettings()
    auth: AuthSettings = TestAuthSettings()
    middleware: MiddlewareSettings = TestMiddlewareSettings()

    api_prefix: str = "/api"
