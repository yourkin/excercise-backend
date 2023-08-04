import logging

from sqlmodel import Session, SQLModel, create_engine

from ex_back.config import get_settings

log = logging.getLogger("uvicorn")

engine = create_engine(get_settings().sync_database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


#
# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session


if __name__ == "__main__":
    create_db_and_tables()
