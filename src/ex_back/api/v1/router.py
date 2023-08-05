from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ex_back.core.concurrency import JobRunner
from ex_back.core.stock_exchange import place_order
from ex_back.database import get_db
from ex_back.models import OrderModel
from ex_back.types import (
    CreateOrderModel,
    CreateOrderResponseModel,
    JobModel,
    OrderWithJobID,
)

router = APIRouter()
runner = JobRunner()


@router.post(
    "/orders",
    status_code=201,
    response_model=OrderWithJobID,
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

    job_id = runner.run(place_order, db_order)

    return {"job_id": job_id, "order": CreateOrderResponseModel.from_orm(db_order)}


@router.get(
    "/jobs/{job_id}",
    response_model=JobModel,
    responses={404: {"description": "Job not found"}},
)
def get_job_status(job_id: str):
    try:
        status = runner.check_status(job_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return JobModel(job_id=job_id, status=status)
