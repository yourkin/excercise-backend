import uuid
from datetime import datetime

import pytest
from starlette.testclient import TestClient

from ex_back.database import create_db_and_tables
from ex_back.main import app
from ex_back.types import Order


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    create_db_and_tables()


@pytest.fixture
def order_id():
    return str(uuid.uuid4())


@pytest.fixture
def job_id():
    return str(uuid.uuid4())


@pytest.fixture
def order_stub(order_id):
    return Order(
        id=order_id,
        created_at=datetime.now(),
        type="limit",
        side="buy",
        instrument="abcdefghijkl",
        limit_price=150.00,
        quantity=10,
    )
