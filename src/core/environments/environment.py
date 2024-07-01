import pathlib
from dataclasses import dataclass
from enum import Enum
from typing import Any

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, PostgresDsn, SecretStr
from starlette.exceptions import HTTPException

from src.api.errors.http_error import http_error_handler
from src.api.errors.validation_error import http422_error_handler


class EnvironmentTypes(Enum):
    base: str = "base"
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class Environment(BaseModel):
    app_env: EnvironmentTypes = EnvironmentTypes.base

    env_file: str
    environment: dict[str, str | None]

    database_url: PostgresDsn

    secret_key: SecretStr

    api_prefix: str
    allow_origins: list[str]
    allow_credentials: bool
    allow_methods: list[str]
    allow_headers: list[str]

    @dataclass
    class FastAPIKwargs:
        debug: bool
        docs_url: str
        openapi_prefix: str
        openapi_url: str
        redoc_url: str
        title: str
        version: str

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.FastAPIKwargs.debug,
            "docs_url": self.FastAPIKwargs.docs_url,
            "openapi_prefix": self.FastAPIKwargs.openapi_prefix,
            "openapi_url": self.FastAPIKwargs.openapi_url,
            "redoc_url": self.FastAPIKwargs.redoc_url,
            "title": self.FastAPIKwargs.title,
            "version": self.FastAPIKwargs.version,
            "exception_handler": {
                HTTPException: http_error_handler,
                RequestValidationError: http422_error_handler,
            },
        }

    @staticmethod
    def get_env_file(name: str) -> pathlib.Path | None:
        current_dir = pathlib.Path().cwd()

        for _ in range(len(current_dir.parents)):
            for file in current_dir.iterdir():
                if file.name == name:
                    return current_dir.joinpath(".env")

            current_dir = current_dir.parent
