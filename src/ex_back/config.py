import logging
from functools import lru_cache

from decouple import config
from pydantic import BaseSettings, PostgresDsn

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = config("ENVIRONMENT", default="dev")
    testing: bool = config("TESTING", default=False, cast=bool)
    database_url: PostgresDsn = config("DATABASE_URL", cast=str)
    test_database_url: PostgresDsn = config("TEST_DATABASE_URL", cast=str)
    rabbit_mq_url: str = config("RABBIT_MQ_URL", default="")
    celery_broker_url: str = config("CELERY_BROKER_URL", default="")

    @property
    def sync_database_url(self) -> str:
        return self.database_url.replace("+asyncpg", "")


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()
