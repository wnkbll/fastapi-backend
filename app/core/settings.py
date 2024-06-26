from functools import lru_cache

from app.core.environments import Environment, EnvironmentTypes, DevelopmentEnvironment, ProductionEnvironment

environments: dict[EnvironmentTypes, type[Environment]] = {
    EnvironmentTypes.dev: DevelopmentEnvironment,
    EnvironmentTypes.prod: ProductionEnvironment,
}


@lru_cache
def get_app_settings():
    app_env = EnvironmentTypes.dev
    settings = environments[app_env]
    return settings()
