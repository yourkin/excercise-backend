from sqlmodel import SQLModel, create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.api.models import OrderDB, CreateOrderModel

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> Session:  # This function should be an async generator
    async with async_session() as session:
        yield session

async def create_order(session: AsyncSession, order: CreateOrderModel):
    db_order = OrderDB(**order.dict())
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)
    return db_order

def create_tables():
    engine_sync = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine_sync)
