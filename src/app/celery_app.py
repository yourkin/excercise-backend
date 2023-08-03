from app.api.models import CreateOrderModel, OrderDB
from celery import Celery
from app.api import stock_exchange
from sqlmodel.ext.asyncio.session import AsyncSession

# Configure Celery to use the RabbitMQ broker
celery_app = Celery('tasks', broker='amqp://user:password@rabbitmq//')

# Celery task for creating an order
@celery_app.task(bind=True, max_retries=3)
def place_order(self, order: dict):
    # simulate the order placement in a stock exchange
    try:
        result = stock_exchange.place_order(order)
        if not result:
            raise Exception('Order placement failed')
    except Exception as e:
        raise self.retry(exc=e, countdown=5)
    return order


@celery_app.task
def create_order(session: AsyncSession, order: CreateOrderModel):
    db_order = OrderDB(**order.dict())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order
