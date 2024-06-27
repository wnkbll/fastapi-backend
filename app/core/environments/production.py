import logging

from dotenv import dotenv_values
from pydantic import PostgresDsn
from dataclasses import dataclass

from app.core.app_logging import logger
from app.core.environments.environment import Environment, EnvironmentTypes


class ProductionEnvironment(Environment):
    app_env: EnvironmentTypes = EnvironmentTypes.prod

    env_file: str = "../.env"
    environment: dict[str, str | None] = dotenv_values(env_file)

    database_url: PostgresDsn = environment["DATABASE_URL"]

    api_prefix: str = "/api"
    allowed_hosts: list[str] = ["*"]

    logger: logging.Logger = logger

    @dataclass
    class FastAPIKwargs:
        debug: bool = False
        docs_url: str = "/docs"
        openapi_prefix: str = ""
        openapi_url: str = "/openapi.json"
        redoc_url: str = "/redoc"
        title: str = "Prod FastAPI pet project"
        version: str = "0.0.0"
