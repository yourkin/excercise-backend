from datetime import datetime

from fastapi import APIRouter

from ex_back.api.models import CreateOrderModel, CreateOrderResponseModel

router = APIRouter()


@router.post(
    "/orders",
    status_code=201,
    response_model=CreateOrderResponseModel,
    response_model_by_alias=True,
)
async def create_order(model: CreateOrderModel):
    fake_response = {
        "id": "123",
        "created_at": datetime.now(),
        "type": model.type_,
        "side": model.side,
        "instrument": model.instrument,
        "limit_price": model.limit_price,
        "quantity": model.quantity,
    }

    return fake_response
