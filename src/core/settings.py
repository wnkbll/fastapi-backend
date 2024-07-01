import logging
from functools import lru_cache

from src.core.app_logging.logger import Logger
from src.core.environments import (
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
def get_app_settings() -> Environment:
    app_env: EnvironmentTypes = EnvironmentTypes.test
    settings = environments[app_env]
    print(settings().database_url)
    return settings()


@lru_cache
def get_app_logger() -> logging.Logger:
    logger = Logger("../logger_config.json").logger
    return logger
