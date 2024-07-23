from functools import lru_cache

from src.core.settings import Settings


@lru_cache
def get_app_settings() -> Settings:
    return Settings()
