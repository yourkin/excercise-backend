import logging

from sqlmodel import SQLModel, create_engine

from app.config import get_settings

log = logging.getLogger("uvicorn")


def create_tables():
    engine_sync = create_engine(get_settings().database_url)
    SQLModel.metadata.create_all(engine_sync)


if __name__ == "__main__":
    create_tables()
