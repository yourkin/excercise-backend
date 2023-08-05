import asyncio

import pytest

from ex_back.core.concurrency import JobRunner, JobStatus
from ex_back.core.stock_exchange import place_order
from ex_back.models import OrderSide, OrderType

job_runner = JobRunner()


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


def test_get_job_status(client, order_stub, job_id):
    job_id = job_runner.run(place_order, order_stub)
    response = client.get(f"/v1/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["status"] in [status.value for status in JobStatus]


def test_get_nonexistent_job_status(client, job_id):
    response = client.get(f"/v1/jobs/{job_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"No job with ID {job_id}"


@pytest.mark.asyncio
async def test_get_completed_job_status(client, order_stub):
    job_id = job_runner.run(place_order, order_stub)

    async def wait_for_job_to_complete():
        while True:
            response = client.get(f"/v1/jobs/{job_id}")
            if response.json()["status"] == JobStatus.COMPLETED.value:
                break
            await asyncio.sleep(0.5)  # sleep for 500 milliseconds before the next check

    # wait for the job to complete, but no longer than 60 seconds
    await asyncio.wait_for(wait_for_job_to_complete(), timeout=60.0)

    response = client.get(f"/v1/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["status"] == JobStatus.COMPLETED.value
