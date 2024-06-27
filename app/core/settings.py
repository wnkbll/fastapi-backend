import logging

from functools import lru_cache

from app.core.app_logging import Logger
from app.core.environments import Environment, EnvironmentTypes, DevelopmentEnvironment, ProductionEnvironment

environments: dict[EnvironmentTypes, type[Environment]] = {
    EnvironmentTypes.dev: DevelopmentEnvironment,
    EnvironmentTypes.prod: ProductionEnvironment,
}


@lru_cache
def get_app_settings() -> Environment:
    app_env = EnvironmentTypes.dev
    settings = environments[app_env]
    return settings()


@lru_cache
def get_app_logger() -> logging.Logger:
    logger = Logger("../logger_config.json").logger
    return logger
