from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> Session:
    async with async_session() as session:
        yield session

def create_tables():
    with create_engine(DATABASE_URL) as engine:
        SQLModel.metadata.create_all(engine)
