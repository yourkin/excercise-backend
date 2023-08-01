from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order():
    response = client.post(
        "/v1/orders",
        json={
            "type": "limit",
            "side": "buy",
            "instrument": "BTCUSD",
            "limit_price": 50000.0,
            "quantity": 1,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["type"] == "limit"
    assert data["side"] == "buy"
    assert data["instrument"] == "BTCUSD"
    assert data["limit_price"] == 50000.0
    assert data["quantity"] == 1
    assert "id" in data
    assert "created_at" in data

def test_create_order_invalid_input():
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
    assert data["detail"][0]["msg"] == "Attribute `limit_price` is required for type `limit`"
