from fastapi import APIRouter

from ex_back.api.models import CreateOrderModel

router = APIRouter()


@router.post(
    "/orders",
    status_code=201,
    # response_model=CreateOrderResponseModel,
    response_model_by_alias=True,
)
async def create_order(model: CreateOrderModel):
    return {"message": "Order is being created"}
