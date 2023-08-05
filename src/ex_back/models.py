import uuid

from sqlalchemy import Column, DateTime, Enum, Float, String, func
from sqlalchemy.dialects.postgresql import UUID

from ex_back.api.types import OrderSide, OrderType
from ex_back.database import Base


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
