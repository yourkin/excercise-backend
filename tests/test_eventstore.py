import json
import time

import pytest

from ex_back.models import EventOutbox
from ex_back.types import EventStatus, EventType
from messaging.tasks.producer import publish_events_to_rabbitmq


def test_create_order(client, order_stub):
    response = client.post("/v1/orders", json=order_stub)
    assert response.status_code == 201
    data = response.json()
    assert "event_id" in data
    assert "created_at" in data
    assert "event_type" in data
    assert "status" in data


def test_list_outbox_events(client):
    response = client.get("/v1/events/outbox")
    assert response.status_code == 200
    data = response.json()
    # Not asserting the contents of the events since this can be dynamic
    assert isinstance(data, list)


def test_get_outbox_event_existing(client, event_id, order_stub):
    # Make a request to the server to get the outbox event by event ID
    response = client.get(f"/v1/events/outbox/{event_id}")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response data matches the expected data
    event = response.json()
    assert event["id"] == event_id
    assert event["event_type"] == "OrderSubmitted"
    assert "event_data" in event
    assert "status" in event
    assert "created_at" in event
    assert "published_at" in event
    assert "failed_at" in event
    assert "error" in event
    assert "metadata_" in event

    event_data = json.loads(event["event_data"])

    # Additional assertions on the event data based on the event itself
    assert "type_" in event_data
    assert "side" in event_data
    assert "instrument" in event_data
    assert "limit_price" in event_data
    assert "quantity" in event_data

    assert event_data["type_"] == order_stub["type"]
    assert event_data["side"] == order_stub["side"]
    assert event_data["instrument"] == order_stub["instrument"]
    assert event_data["limit_price"] == str(
        order_stub["limit_price"]
    )  # Convert Decimal to str
    assert event_data["quantity"] == order_stub["quantity"]


def test_get_outbox_event_nonexistent(client):
    nonexistent_event_id = 99999999  # Assuming this doesn't exist
    response = client.get(f"/v1/events/outbox/{nonexistent_event_id}")
    assert response.status_code == 404


def test_list_store_events(client):
    response = client.get("/v1/events/store")
    assert response.status_code == 200
    data = response.json()
    # Not asserting the contents of the events since this can be dynamic
    assert isinstance(data, list)


def test_get_store_event_existing(client, store_event_id, order_stub):
    # Make a request to the server to get the store event by event ID
    response = client.get(f"/v1/events/store/{store_event_id}")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response data matches the expected data
    event = response.json()
    assert event["id"] == store_event_id
    assert event["event_type"] == "OrderSubmitted"
    assert "event_data" in event
    assert "occurred_at" in event
    assert "version" in event
    assert "aggregate_id" in event
    assert "metadata_" in event

    # Parse the stringified event_data into a dictionary
    event_data = json.loads(event["event_data"])

    # Additional assertions on the event data based on the event itself
    assert "type_" in event_data
    assert "side" in event_data
    assert "instrument" in event_data
    assert "limit_price" in event_data
    assert "quantity" in event_data

    assert event_data["type_"] == order_stub["type"]
    assert event_data["side"] == order_stub["side"]
    assert event_data["instrument"] == order_stub["instrument"]
    assert event_data["limit_price"] == str(
        order_stub["limit_price"]
    )  # Convert Decimal to str
    assert event_data["quantity"] == order_stub["quantity"]


def test_get_store_event_nonexistent(client):
    nonexistent_event_id = 99999999  # Assuming this doesn't exist
    response = client.get(f"/v1/events/store/{nonexistent_event_id}")
    assert response.status_code == 404


@pytest.mark.skip(reason="Needs updating")
def test_event_marked_as_published(client, order_stub, test_db_session):
    # Preparing a mock event in outbox
    with test_db_session:
        mock_event_metadata = {
            "source": "web",  # just an example, you can define metadata according to your requirements
        }
        mock_event = EventOutbox(
            event_type=EventType.ORDER_CREATED,
            event_data=order_stub,
            status=EventStatus.PENDING,
            metadata_=mock_event_metadata,  # Optional, you can remove if not needed
        )
        test_db_session.add(mock_event)
        test_db_session.commit()
        event_id = mock_event.id

    # Trigger the Celery task directly to process the outbox event
    publish_events_to_rabbitmq.apply_async(
        (True,)
    )  # If you're passing any args to the task, do it here

    # Wait for task completion
    time.sleep(10)

    # Check that the event has been marked as PUBLISHED
    with test_db_session:
        event = test_db_session.query(EventOutbox).filter_by(id=event_id).first()
        assert event is not None, "Event not found in the database"
        assert (
            event.status == EventStatus.PUBLISHED
        ), f"Expected status PUBLISHED but got {event.status}"
