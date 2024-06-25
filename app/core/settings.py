from typing import Type
from functools import lru_cache

from app.core.environments import DevelopmentEnvironment
from app.core.environments import Environment, EnvironmentTypes

environments: dict[EnvironmentTypes, Type[Environment]] = {
    EnvironmentTypes.dev: DevelopmentEnvironment,
}


@lru_cache
def get_app_settings():
    app_env = EnvironmentTypes.dev
    settings = environments[app_env]
    return settings()
