import uuid

import pytest
from starlette.testclient import TestClient

from ex_back.database import create_db_and_tables
from ex_back.main import app
from ex_back.models import OrderSide, OrderType


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    create_db_and_tables()


@pytest.fixture
def order_id():
    return str(uuid.uuid4())


@pytest.fixture(scope="function")
def job_id(client, order_stub):
    job_id = client.post("/v1/orders/", json=order_stub).json()["job_id"]
    return job_id


@pytest.fixture
def order_stub(order_id):
    order_data = {
        "type": OrderType.LIMIT.value,
        "side": OrderSide.BUY.value,
        "instrument": "abcdefghijkl",
        "limit_price": 150.00,
        "quantity": 10,
    }
    return order_data
