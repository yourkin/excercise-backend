from fastapi import APIRouter, Depends, HTTPException
from app.api.database import get_session, create_order
from app.api.models import CreateOrderModel, CreateOrderResponseModel
from app.api.stock_exchange import place_order, OrderPlacementError
from app.api.types import Order

router = APIRouter()


@router.post(
    "/orders",
    status_code=201,
    response_model=CreateOrderResponseModel,
    response_model_by_alias=True,
)
async def create_order(model: CreateOrderModel, session=Depends(get_session)):
    db_order = await create_order(session, model)

    try:
        place_order(Order(**db_order.dict()))
    except OrderPlacementError:
        raise HTTPException(status_code=500, detail="Internal server error while placing the order")

    return db_order
