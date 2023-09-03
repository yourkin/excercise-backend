import json
from typing import Optional

import pika

from ex_back.config import get_settings


class RabbitMQManager:
    def __init__(
        self,
        host: str,
        queue_name: str,
        exchange_type: str = "direct",
        exchange_name: str = "",
    ):
        self._host: str = host
        self._queue_name: str = queue_name
        self._exchange_name: str = exchange_name
        self._exchange_type: str = exchange_type
        self._connection: pika.BlockingConnection = None
        self._channel: pika.Channel = None

    def __enter__(self) -> "RabbitMQManager":
        credentials = pika.PlainCredentials(
            username=get_settings().rabbitmq_user, password=get_settings().rabbitmq_pass
        )
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._host, credentials=credentials)
        )
        self._channel = self._connection.channel()

        # Declare exchange
        self._channel.exchange_declare(
            exchange=self._exchange_name,
            exchange_type=self._exchange_type,
            durable=True,
        )

        # For fanout exchanges, we don't need to declare a queue or bind it to the exchange
        if self._exchange_type != "fanout":
            # Declare queue
            self._channel.queue_declare(queue=self._queue_name, durable=True)

            # Bind the queue to the exchange
            self._channel.queue_bind(
                exchange=self._exchange_name, queue=self._queue_name
            )

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._connection:
            self._connection.close()

    def publish(self, event: dict) -> None:
        event_data = json.dumps(event)
        self._channel.basic_publish(
            exchange=self._exchange_name,
            routing_key=self._queue_name,
            body=event_data.encode("utf-8"),  # Convert string to bytes
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            ),
        )

    def consume_message(self) -> Optional[dict]:
        method_frame, header_frame, body = self._channel.basic_get(self._queue_name)
        if method_frame:
            self._channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body.decode("utf-8"))
        return None

    def consume_messages(self, callback, no_ack=False) -> None:
        """
        Consume messages indefinitely using a callback function.
        :param callback: A function that will be called with each message's data.
        :param no_ack: If True, no acknowledgment will be required for the messages.
        """

        def _callback(ch, method, properties, body):
            message = json.loads(body.decode("utf-8"))
            callback(message)

        self._channel.basic_consume(
            queue=self._queue_name, on_message_callback=_callback, auto_ack=no_ack
        )
        self._channel.start_consuming()
