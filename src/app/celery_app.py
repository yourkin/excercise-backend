from celery import Celery
from app.api import stock_exchange

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
