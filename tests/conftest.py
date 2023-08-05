import pytest
from starlette.testclient import TestClient

from ex_back.database import create_db_and_tables
from ex_back.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    create_db_and_tables()
