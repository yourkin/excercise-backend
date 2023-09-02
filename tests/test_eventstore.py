import json


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
