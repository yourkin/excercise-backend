import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from event_publisher.app import app
from event_publisher.messaging.rabbitmq_publisher import RabbitMQPublisher
from ex_back.config import get_settings
from ex_back.database import engine
from shared.managers import EventStoreManager, OutboxEventManager

logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)


@app.task
def publish_events_to_rabbitmq(use_test_db: bool = False):
    if use_test_db:
        TEST_DATABASE_URL = get_settings().sync_test_database_url
        engine = create_engine(TEST_DATABASE_URL)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with Session() as session:
        event_store_manager = EventStoreManager(session)
        outbox_event_manager = OutboxEventManager(session)
        unprocessed_outbox_events = outbox_event_manager.get_unprocessed_events()

        if not unprocessed_outbox_events:
            logger.info("No unprocessed events found.")
            return

        with RabbitMQPublisher(
            host=get_settings().rabbitmq_host,
            queue_name="order",
            exchange_name="order_exchange",
        ) as publisher:
            for outbox_event in unprocessed_outbox_events:
                try:
                    with session.begin_nested():  # Begin a nested transaction
                        publisher.publish(outbox_event.event_data)
                        outbox_event_manager.mark_as_processed(outbox_event)
                        event_store_manager.save(outbox_event)
                except Exception as e:
                    logger.error(
                        f"Failed to process event {outbox_event.id}. Error: {e}"
                    )
                    outbox_event_manager.mark_as_failed(outbox_event, str(e))
            session.commit()  # Commit the outer transaction
