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


def test_create_order_invalid_input(client):
    response = client.post(
        "/v1/orders",
        json={
            "type": "limit",
            "side": "buy",
            "instrument": "BTCUSD",
            "quantity": 1,
        },
    )
    assert response.status_code == 422
    data = response.json()
    assert (
        data["detail"][0]["msg"]
        == "Attribute `limit_price` is required for type `limit`"
    )
