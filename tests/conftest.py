import pytest as pytest
from starlette.testclient import TestClient

from ex_back.api.v1.router import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
