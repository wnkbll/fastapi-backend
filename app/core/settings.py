import logging
from functools import lru_cache

from app.core.app_logging.logger import Logger
from app.core.environments import (
    Environment,
    EnvironmentTypes,
    DevelopmentEnvironment,
    ProductionEnvironment,
    TestEnvironment,
)

environments: dict[EnvironmentTypes, type[Environment]] = {
    EnvironmentTypes.dev: DevelopmentEnvironment,
    EnvironmentTypes.prod: ProductionEnvironment,
    EnvironmentTypes.test: TestEnvironment,
}


@lru_cache
def get_app_settings(app_env: EnvironmentTypes = EnvironmentTypes.dev) -> Environment:
    settings = environments[app_env]
    return settings()


@lru_cache
def get_app_logger() -> logging.Logger:
    logger = Logger("../logger_config.json").logger
    return logger
