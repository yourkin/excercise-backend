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
    rabbitmq_host: str = config("RABBITMQ_HOST", cast=str)
    rabbitmq_port: str = config("RABBITMQ_PORT", cast=str)
    rabbitmq_user: str = config("RABBITMQ_DEFAULT_USER", cast=str)
    rabbitmq_pass: str = config("RABBITMQ_DEFAULT_PASS", cast=str)

    @property
    def broker_url(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_pass}@{self.rabbitmq_host}:{self.rabbitmq_port}//"

    @property
    def sync_database_url(self) -> str:
        return self.database_url.replace("+asyncpg", "")

    @property
    def sync_test_database_url(self) -> str:
        return self.test_database_url.replace("+asyncpg", "")


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()
