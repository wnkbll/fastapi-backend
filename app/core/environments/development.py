import pathlib

from dotenv import dotenv_values
from pydantic import PostgresDsn
from dataclasses import dataclass

from app.core.environments.environment import Environment, EnvironmentTypes


class DevelopmentEnvironment(Environment):
    app_env: EnvironmentTypes = EnvironmentTypes.dev

    env_file: pathlib.Path = Environment.get_env_file()
    environment: dict[str, str | None] = dotenv_values(env_file)

    database_url: PostgresDsn = environment["DATABASE_URL"]

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
        title: str = "Dev FastAPI pet project"
        version: str = "0.0.0"
