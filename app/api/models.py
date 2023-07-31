from datetime import datetime

from pydantic import BaseModel, Field, condecimal, conint, constr, root_validator
from typing import Optional

from sqlmodel import SQLModel, Field

from app.api.types import Order, OrderSide, OrderType


class CreateOrderModel(BaseModel):
    type_: OrderType = Field(..., alias="type")
    side: OrderSide
    instrument: constr(min_length=12, max_length=12)
    limit_price: Optional[condecimal(decimal_places=2)]
    quantity: conint(gt=0)

    @root_validator
    def validator(cls, values: dict):
        if values.get("type_") == "market" and values.get("limit_price"):
            raise ValueError(
                "Providing a `limit_price` is prohibited for type `market`"
            )

        if values.get("type_") == "limit" and not values.get("limit_price"):
            raise ValueError("Attribute `limit_price` is required for type `limit`")

        return values


class CreateOrderResponseModel(Order):
    pass


class Order(SQLModel, table=True):
    id_: int = Field(default=None, alias="id", primary_key=True)
    created_at: datetime
    type_: str = Field(..., alias="type")
    side: str
    instrument: str
    limit_price: Optional[float]
    quantity: int
