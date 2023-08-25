import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ex_back.config import get_settings
from ex_back.database import Base, get_db
from ex_back.main import app
from ex_back.models import OrderSide, OrderType

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


@pytest.fixture
def client() -> TestClient:
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


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
