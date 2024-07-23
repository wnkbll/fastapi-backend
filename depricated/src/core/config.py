#
# from src.core.environments import Environment, EnvironmentTypes, DevelopmentEnvironment, TestEnvironment
#
# environments: dict[EnvironmentTypes, type[Environment]] = {
#     EnvironmentTypes.dev: DevelopmentEnvironment,
#     EnvironmentTypes.test: TestEnvironment,
# }
#
#
# @lru_cache
# def get_app_settings(env_type: EnvironmentTypes):
#     environment: type[Environment] = environments[env_type]
#     return environment()
from functools import lru_cache

from pydantic import BaseModel, Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from depricated.src.core import ENV_PATH


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding='utf-8', validate_default=False, extra="ignore",
    )

    secret_key: str = Field(validation_alias="SECRET_KEY")


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding='utf-8', validate_default=False, extra="ignore",
    )

    host: str = Field(validation_alias="REDIS_HOST")
    port: str = Field(validation_alias="REDIS_PORT")


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding='utf-8', validate_default=False, extra="ignore",
    )

    user: str = Field(validation_alias="POSTGRES_USER")
    password: str = Field(validation_alias="POSTGRES_PASSWORD")
    host: str = Field(validation_alias="POSTGRES_HOST")
    port: str = Field(validation_alias="POSTGRES_PORT")
    name: str = Field(validation_alias="POSTGRES_NAME")


class FastAPISettings(BaseModel):
    debug: bool = True
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI pet project"
    version: str = "0.0.0"


class LoggingSettings(BaseModel):
    file: str = "backend.log"
    rotation: str = "2MB"
    compression: str = "zip"


class MiddlewareSettings(BaseModel):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class Settings(BaseModel):
    auth: AuthSettings = AuthSettings()
    redis: RedisSettings = RedisSettings()
    postgres: PostgresSettings = PostgresSettings()

    fastapi: FastAPISettings = FastAPISettings()
    logging: LoggingSettings = LoggingSettings()
    middleware: MiddlewareSettings = MiddlewareSettings()

    api_prefix: str = "/api"

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres.user}:{self.postgres.password}@"
            f"{self.postgres.host}:{self.postgres.port}/"
            f"{self.postgres.name}"
        )

    @property
    def redis_dsn(self) -> RedisDsn:
        return (
            f"redis://{self.redis.host}:{self.redis.port}"
        )

    @property
    def fastapi_kwargs(self) -> dict[str, any]:
        return self.fastapi.model_dump()


@lru_cache
def get_settings() -> Settings:
    return Settings()
