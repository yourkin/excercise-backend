from celery import Celery
from app.api.database import create_order as create_order_db
from app.api.models import CreateOrderModel
from sqlalchemy.ext.asyncio import AsyncSession

# Configure Celery to use the Redis broker
celery_app = Celery('tasks', broker='pyamqp://guest@localhost//')

# Celery task for creating an order
@celery_app.task
async def create_order(session: AsyncSession, order: dict):
    model = CreateOrderModel.parse_obj(order)
    await create_order_db(session, model)
