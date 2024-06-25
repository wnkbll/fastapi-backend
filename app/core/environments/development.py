from dotenv import dotenv_values
from pydantic import PostgresDsn
from dataclasses import dataclass

from app.core.environments import Environment, EnvironmentTypes


class DevelopmentEnvironment(Environment):
    app_env: EnvironmentTypes = EnvironmentTypes.dev

    env_file: str = "../.env"
    environment: dict[str, str | None] = dotenv_values(env_file)

    database_url: PostgresDsn = environment["DATABASE_URL"]

    api_prefix: str = "/api"
    allowed_hosts: list[str] = ["*"]

    @dataclass
    class FastAPIKwargs:
        debug: bool = True
        docs_url: str = "/docs"
        openapi_prefix: str = ""
        openapi_url: str = "/openapi.json"
        redoc_url: str = "/redoc"
        title: str = "FastAPI pet project"
        version: str = "0.0.0"
