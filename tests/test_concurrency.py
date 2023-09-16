import asyncio

import pytest

from ex_back.core.concurrency import JobStatus


@pytest.mark.skip(reason="Functionality not yet updated")
def test_create_order_with_job_id(client, order_stub):
    # Make a request to the server
    response = client.post("/v1/orders/", json=order_stub)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201
    # Assert that the job_id is present in the response
    assert "job_id" in response.json()
    # Assert that the order data is present in the response
    assert "order" in response.json()


@pytest.mark.skip(reason="Functionality not yet updated")
def test_get_job_status(client, order_stub, job_id):
    response = client.get(f"/v1/jobs/{job_id}")
    assert response.json()["job_id"] == job_id
    assert response.status_code == 200
    assert response.json()["status"] in [status.value for status in JobStatus]


@pytest.mark.skip(reason="Functionality not yet updated")
def test_get_nonexistent_job_status(client, order_id, order_stub):
    response = client.get(
        f"/v1/jobs/{order_id}"
    )  # deliberately using order_id to check for the error
    assert response.status_code == 404
    assert response.json()["detail"] == f"No job with ID {order_id}"


@pytest.mark.skip(reason="Functionality not yet updated")
@pytest.mark.asyncio
async def test_get_completed_job_status(client, job_id, order_stub):
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
