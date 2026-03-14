import os
from functools import lru_cache

from core.logger import get_logger

logger = get_logger(__name__)


class Settings:
    def __init__(self):
        self.app_name = os.getenv("APP_NAME", "undefined")

        logger.info(f"APP_NAME: {self.app_name}")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
