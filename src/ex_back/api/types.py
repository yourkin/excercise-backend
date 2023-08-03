from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, condecimal, conint, constr


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"


class Order(BaseModel):
    # id generated by the database
    id_: str = Field(..., alias="id")
    created_at: datetime

    type_: OrderType = Field(..., alias="type")
    side: OrderSide
    instrument: constr(min_length=12, max_length=12)
    limit_price: Optional[condecimal(decimal_places=2)]
    quantity: conint(gt=0)
