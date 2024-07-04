from functools import lru_cache

from src.core.environments import Environment, EnvironmentTypes, DevelopmentEnvironment

environments: dict[EnvironmentTypes, type[Environment]] = {
    EnvironmentTypes.dev: DevelopmentEnvironment,
}


@lru_cache
def get_app_settings(env_type: EnvironmentTypes):
    environment: type[Environment] = environments[env_type]
    return environment()
