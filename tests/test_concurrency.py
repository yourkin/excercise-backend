from ex_back.models import OrderSide, OrderType


def test_create_order_with_job_id(client):
    # Test data
    order_data = {
        "type": OrderType.LIMIT.value,
        "side": OrderSide.BUY.value,
        "instrument": "abcdefghijkl",
        "limit_price": 150.00,
        "quantity": 10,
    }
    # Make a request to the server
    response = client.post("/v1/orders/", json=order_data)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201
    # Assert that the job_id is present in the response
    assert "job_id" in response.json()
    # Assert that the order data is present in the response
    assert "order" in response.json()
