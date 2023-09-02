import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ex_back.database import get_db
from ex_back.models import OrderModel
from ex_back.types import (
    CreateOrderModel,
    CreateOrderResponse,
    CreateOrderResponseModel,
    EventOutboxResponse,
    EventType,
    OrderCreated,
)
from shared.managers import OutboxEventManager

router = APIRouter()


@router.post(
    "/orders",
    status_code=201,
    response_model=CreateOrderResponse,
    response_model_by_alias=True,
)
async def create_order(
    model: CreateOrderModel, db: Session = Depends(get_db)
) -> CreateOrderResponse:
    # Create event for order creation
    event = OrderCreated(
        id_=uuid.uuid4(),
        type=model.type_,
        side=model.side,
        instrument=model.instrument,
        limit_price=model.limit_price,
        quantity=model.quantity,
    )
    # Using manager to store the event
    manager = OutboxEventManager(db)
    outbox_event = manager.save(EventType.ORDER_SUBMITTED, event.json())

    # The actual handling of the event will be done by an asynchronous worker
    # that processes the events in the outbox table

    response = CreateOrderResponse(
        event_id=outbox_event.id,
        created_at=outbox_event.created_at,
        event_type=outbox_event.event_type,
        status=outbox_event.status,
    )

    return response


@router.get(
    "/events/outbox",
    response_model=List[EventOutboxResponse],
    response_model_by_alias=True,
)
def list_outbox_events(db: Session = Depends(get_db)) -> List[EventOutboxResponse]:
    manager = OutboxEventManager(db)
    outbox_events = manager.get_all_events()

    # Convert SQLAlchemy model instances to Pydantic model instances
    event_responses = [EventOutboxResponse.from_orm(event) for event in outbox_events]

    return event_responses


@router.get(
    "/events/outbox/{event_id}",
    response_model=EventOutboxResponse,
    response_model_by_alias=True,
)
def get_outbox_event(
    event_id: int, db: Session = Depends(get_db)
) -> EventOutboxResponse:
    manager = OutboxEventManager(db)
    outbox_event = manager.get_event_by_id(event_id)

    if not outbox_event:
        raise HTTPException(status_code=404, detail="Event not found")

    return EventOutboxResponse.from_orm(outbox_event)


@router.get(
    "/orders",
    response_model=List[CreateOrderResponseModel],
    response_model_by_alias=True,
)
def list_orders(db: Session = Depends(get_db)) -> List[CreateOrderResponseModel]:
    db_orders = db.query(OrderModel).all()
    return [CreateOrderResponseModel.from_orm(order) for order in db_orders]
