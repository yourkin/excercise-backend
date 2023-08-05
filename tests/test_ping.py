def test_read_ping(client):
    # Test the ping endpoint for a 200 response and the correct response body as a minimal health check.
    # If this doesn't work, nothing else will.
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
