from fastapi import APIRouter, Depends, HTTPException
from app.api.database import get_session
from app.api.models import CreateOrderModel, CreateOrderResponseModel
from app.api.stock_exchange import place_order, OrderPlacementError
from app.api.types import Order
from app.celery_app import create_order

router = APIRouter()


@router.post(
    "/orders",
    status_code=201,
    response_model=CreateOrderResponseModel,
    response_model_by_alias=True,
)
async def create_order_endpoint(model: CreateOrderModel, session=Depends(get_session)):
    # Create order in the background using Celery
    create_order.delay(session, model.dict())

    # Place the order in the stock exchange
    try:
        place_order(Order(**model.dict()))
    except OrderPlacementError:
        raise HTTPException(status_code=500, detail="Internal server error while placing the order")

    return {"message": "Order is being created"}
