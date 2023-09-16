import logging
from functools import lru_cache

from decouple import config
from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = config("ENVIRONMENT")
    db_user: str = config("POSTGRES_USER", cast=str)
    db_password: str = config("POSTGRES_PASSWORD", cast=str)
    db_host: str = config("PG_HOST", cast=str)
    db_port: int = config("PG_PORT", cast=int)
    db_name: str = config("PG_DB", cast=str)
    test_db: str = config("TEST_DB", cast=str)
    testing: bool = config("TESTING", cast=bool, default=False)
    rabbitmq_host: str = config("RABBITMQ_HOST", cast=str)
    rabbitmq_port: str = config("RABBITMQ_PORT", cast=int)
    rabbitmq_user: str = config("RABBITMQ_DEFAULT_USER", cast=str)
    rabbitmq_pass: str = config("RABBITMQ_DEFAULT_PASS", cast=str)

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def test_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.test_db}"

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
