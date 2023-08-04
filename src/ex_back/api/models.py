import uuid

from sqlalchemy import Column, Enum, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from ex_back.api.types import OrderSide, OrderType
from ex_back.database import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    type_ = Column(Enum(OrderType), nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    instrument = Column(String, nullable=False)
    limit_price = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False)
