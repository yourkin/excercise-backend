from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ex_back.core.stock_exchange import OrderPlacementError, place_order
from ex_back.database import get_db
from ex_back.models import OrderModel
from ex_back.types import CreateOrderModel, CreateOrderResponseModel

router = APIRouter()


@router.post(
    "/orders",
    status_code=201,
    response_model=CreateOrderResponseModel,
    response_model_by_alias=True,
)
async def create_order(model: CreateOrderModel, db: Session = Depends(get_db)):
    # Convert the Pydantic model to SQLAlchemy model
    db_order = OrderModel(
        type=model.type_,
        side=model.side,
        instrument=model.instrument,
        limit_price=model.limit_price,
        quantity=model.quantity,
    )
    db.add(db_order)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while trying to create order. Detail: {e}",
        )
    db.refresh(db_order)
    try:
        place_order(db_order)
    except OrderPlacementError as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error while placing the order"},
        )
    return CreateOrderResponseModel.from_orm(db_order)
