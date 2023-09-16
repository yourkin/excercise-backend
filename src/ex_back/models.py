import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Enum, Float, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

from ex_back.database import Base
from ex_back.types import EventStatus, EventType, OrderSide, OrderType


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    type = Column(Enum(OrderType), nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    instrument = Column(String, nullable=False)
    limit_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)


class EventOutbox(Base):
    __tablename__ = "outbox"
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(Enum(EventType), nullable=False)
    event_data = Column(JSONB, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    failed_at = Column(DateTime, nullable=True)
    error = Column(String(255), nullable=True)
    metadata_ = Column(JSONB, nullable=True)


class EventStore(Base):
    __tablename__ = "event_store"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_type = Column(String(50), nullable=False)
    event_data = Column(JSONB, nullable=False)
    occurred_at = Column(DateTime, default=datetime.utcnow)
    version = Column(Integer, nullable=False, default=1)
    aggregate_id = Column(UUID, nullable=True)
    metadata_ = Column(JSONB, nullable=True)
