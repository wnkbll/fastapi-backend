import pathlib
from dataclasses import dataclass

from dotenv import dotenv_values
from pydantic import PostgresDsn, SecretStr

from src.core.environments.environment import Environment, EnvironmentTypes


class TestEnvironment(Environment):
    app_env: EnvironmentTypes = EnvironmentTypes.test

    env_file: pathlib.Path = Environment.get_env_file("test.env")
    environment: dict[str, str | None] = dotenv_values(env_file)

    database_url: PostgresDsn = environment["DATABASE_URL"]
    secret_key: SecretStr = SecretStr(environment["SECRET_KEY"])

    api_prefix: str = "/api"
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    allow_headers: list[str] = [
        "Accept", "Accept-Language", "Content-Language", "Content-Type",
    ]

    @dataclass
    class FastAPIKwargs:
        debug: bool = True
        docs_url: str = "/docs"
        openapi_prefix: str = ""
        openapi_url: str = "/openapi.json"
        redoc_url: str = "/redoc"
        title: str = "Test FastAPI pet project"
        version: str = "0.0.0"
