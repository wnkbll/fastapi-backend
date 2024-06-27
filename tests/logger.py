from app.core import get_app_settings

settings = get_app_settings()
logger = settings.logger

logger.info("Some info")
