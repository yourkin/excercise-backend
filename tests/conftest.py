import pytest as pytest
from starlette.testclient import TestClient

from ex_back.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
