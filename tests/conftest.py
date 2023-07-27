import pytest as pytest
from starlette.testclient import TestClient

from app.api.v1.router import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
