from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel, create_engine

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> Session:
    async with async_session() as session:
        yield session


def create_tables():
    engine_sync = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine_sync)
