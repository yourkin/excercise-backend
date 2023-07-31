from fastapi import APIRouter

from app.api.database import get_session
from app.api.models import CreateOrderModel, CreateOrderResponseModel

router = APIRouter()

@router.post(
    "/orders",
    status_code=201,
    response_model=CreateOrderResponseModel,
    response_model_by_alias=True,
)
async def create_order(model: CreateOrderModel):
    raise NotImplementedError()
