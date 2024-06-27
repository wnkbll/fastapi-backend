from app.core.app_logging._logger import Logger

logger = Logger("../logger_config.json").logger

__all__ = [
    "logger",
]
