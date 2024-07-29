from pydantic import BaseModel, Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.paths import ENV_PATH

settings_config_dict = SettingsConfigDict(
    env_file=ENV_PATH, env_file_encoding='utf-8', validate_default=False, extra="ignore",
)


class AuthSettings(BaseSettings):
    model_config = settings_config_dict

    secret_key: str = Field(validation_alias="SECRET_KEY")


class RedisSettings(BaseSettings):
    model_config = settings_config_dict

    host: str = Field(validation_alias="REDIS_HOST")
    port: str = Field(validation_alias="REDIS_PORT")


class PostgresSettings(BaseSettings):
    model_config = settings_config_dict

    user: str = Field(validation_alias="DB_USER")
    password: str = Field(validation_alias="DB_PASS")
    host: str = Field(validation_alias="DB_HOST")
    port: str = Field(validation_alias="DB_PORT")
    name: str = Field(validation_alias="DB_NAME")


class FastAPISettings(BaseModel):
    debug: bool = True
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI pet project"
    version: str = "0.1.0"


class LoggingSettings(BaseModel):
    file: str = "backend.log"
    rotation: str = "2MB"
    compression: str = "zip"


class MiddlewareSettings(BaseModel):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class PrefixSettings(BaseModel):
    api_prefix: str = "/api"
    tasks_prefix: str = "tasks"


class Settings(BaseModel):
    auth: AuthSettings = AuthSettings()
    redis: RedisSettings = RedisSettings()
    postgres: PostgresSettings = PostgresSettings()

    fastapi: FastAPISettings = FastAPISettings()
    logging: LoggingSettings = LoggingSettings()
    middleware: MiddlewareSettings = MiddlewareSettings()
    prefixes: PrefixSettings = PrefixSettings()

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
        return f"redis://{self.redis.host}:{self.redis.port}"

    @property
    def fastapi_kwargs(self) -> dict[str, any]:
        return self.fastapi.model_dump()

    @property
    def middleware_kwargs(self) -> dict[str, any]:
        return self.middleware.model_dump()
