import logging

from ex_back.config import get_settings
from messaging.app import app
from shared.managers.messaging import RabbitMQManager

logger = logging.getLogger(__name__)


def process_order_message(message: dict):
    logger.info(f"Received order: {message}")


@app.task
def consume_order_messages():
    with RabbitMQManager(
        host=get_settings().rabbitmq_host,
        queue_name="order",
        exchange_name="order_exchange",
    ) as rabbit_manager:
        rabbit_manager.consume_messages(callback=process_order_message, no_ack=True)
