import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from event_publisher.tasks.order_tasks import publish_events_to_rabbitmq
from ex_back.config import get_settings
from ex_back.database import Base, get_db
from ex_back.main import app
from ex_back.models import EventStore, OrderSide, OrderType

TEST_DATABASE_URL = get_settings().sync_test_database_url

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client() -> TestClient:
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="module")
def event_id(client, order_stub):
    # Create an order and obtain its ID
    response = client.post("/v1/orders/", json=order_stub)
    return response.json()["event_id"]


@pytest.fixture(scope="module")
def store_event_id(client, event_id):
    # Trigger the Celery task directly to process the outbox event
    publish_events_to_rabbitmq.apply_async((True,))

    session = next(override_get_db())
    # Fetch the event from the event store using the outbox event data.
    with session:
        event = (
            session.query(EventStore).filter_by(event_type="OrderSubmitted").first()
        )  # This assumes unique event type
        if not event:
            raise Exception("Failed to find the event in the event store")
        return event.id


#
# @pytest.fixture(scope="function")
# def job_id(client, order_stub):
#     job_id = client.post("/v1/orders/", json=order_stub).json()["job_id"]
#     return job_id


@pytest.fixture(scope="session")
def order_stub():
    order_data = {
        "type": OrderType.LIMIT.value,
        "side": OrderSide.BUY.value,
        "instrument": "abcdefghijkl",
        "limit_price": 150.00,
        "quantity": 10,
    }
    return order_data


@pytest.fixture(scope="session")
def test_db_session():
    return next(get_db(use_test_db=True))
