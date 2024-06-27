import logging

from enum import Enum
from typing import Any
from dataclasses import dataclass
from pydantic import BaseModel, PostgresDsn


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

    api_prefix: str
    allowed_hosts: list[str]

    logger: logging.Logger

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
        }
