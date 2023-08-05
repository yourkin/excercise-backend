from unittest import mock


def test_create_order_failure(client):
    # Patch the random.random to always return 0.91 (i.e., always raise an OrderPlacementError)
    with mock.patch("random.random", return_value=0.91):
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

        # Assert that the response status code is 500 (Internal Server Error)
        assert response.status_code == 500
        # Assert that the error message is correct
        assert response.json() == {
            "message": "Internal server error while placing the order"
        }
