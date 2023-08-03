import logging
import os
from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", False)
    database_url: PostgresDsn = os.environ.get("DATABASE_URL")
    rabbit_mq_url: str = os.environ.get("RABBIT_MQ_URL")
    celery_broker_url: str = os.environ.get("CELERY_BROKER_URL")


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()
