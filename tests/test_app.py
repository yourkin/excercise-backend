from datetime import datetime

import dateutil.parser


def test_create_order(client):
    # Test data
    order_data = {
        "type": "limit",
        "side": "buy",
        "instrument": "abcdefghijkl",
        "limit_price": 150.00,
        "quantity": 10,
    }
    # Make a request to the server
    response = client.post("/v1/orders/", json=order_data)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert that the response data matches the test data
    response_data = response.json()
    assert response_data["type"] == order_data["type"]
    assert response_data["side"] == order_data["side"]
    assert response_data["instrument"] == order_data["instrument"]
    assert response_data["limit_price"] == order_data["limit_price"]
    assert response_data["quantity"] == order_data["quantity"]

    # Parse string to datetime object
    created_at = dateutil.parser.parse(response_data["created_at"])
    assert isinstance(created_at, datetime)


def test_create_order_invalid_limit_price_market_order(client):
    data = {
        "type": "market",
        "side": "buy",
        "instrument": "ABCDEF123456",
        "limit_price": 100.0,
        "quantity": 10,
    }
    response = client.post("/v1/orders", json=data)
    assert response.status_code == 422
    assert "Providing a `limit_price` is prohibited for type `market`" in str(
        response.content
    )


def test_create_order_missing_limit_price_limit_order(client):
    data = {
        "type": "limit",
        "side": "buy",
        "instrument": "ABCDEF123456",
        "quantity": 10,
    }
    response = client.post("/v1/orders", json=data)
    assert response.status_code == 422
    assert "Attribute `limit_price` is required for type `limit`" in str(
        response.content
    )


def test_create_order_invalid_instrument(client):
    data = {
        "type": "market",
        "side": "buy",
        "instrument": "ABC",  # invalid instrument
        "quantity": 10,
    }
    response = client.post("/v1/orders", json=data)
    assert response.status_code == 422
    assert "ensure this value has at least 12 characters" in str(response.content)


def test_create_order_invalid_quantity(client):
    data = {
        "type": "market",
        "side": "buy",
        "instrument": "ABCDEF123456",
        "quantity": 0,  # invalid quantity
    }
    response = client.post("/v1/orders", json=data)
    assert response.status_code == 422
    assert "ensure this value is greater than 0" in str(response.content)
