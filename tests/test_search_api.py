import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.security import REQUEST_LOGS

client = TestClient(app)

STARK_HEADERS = {"X-API-Key": "api-key-stark-industries"}
WAYNE_HEADERS = {"X-API-Key": "api-key-wayne-enterprises"}

@pytest.fixture(autouse=True)
def clean_rate_limit_logs():
    """
    This is a pytest fixture. The `autouse=True` flag means it will
    automatically run before EVERY test function in this file.

    It ensures that the state of the rate limiter is clean before each
    test, preventing one test from affecting another.
    """
    REQUEST_LOGS.clear()
    yield

def test_search_stark_industries_success():
    """Test a successful search for Stark Industries."""
    response = client.get("/search/?q=tony", headers=STARK_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert list(data[0].keys()) == ["email", "department", "position", "location", "employee_ssn"]
    assert data[0]["email"] == "tony.stark@stark.com"

def test_data_isolation():
    """Ensure Stark Industries cannot see Wayne Enterprises' data."""
    response = client.get("/search/?q=bruce", headers=STARK_HEADERS)
    assert response.status_code == 200
    assert response.json() == []

def test_dynamic_columns_for_wayne_enterprises():
    """Test that Wayne Enterprises gets its own configured columns."""
    response = client.get("/search/?q=lucius", headers=WAYNE_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert list(data[0].keys()) == ["first_name", "last_name", "location"]
    assert data[0]["first_name"] == "Lucius"

def test_unauthorized_no_key():
    """Test that requests without an API key are rejected."""
    response = client.get("/search/")
    assert response.status_code == 401

def test_unauthorized_invalid_key():
    """Test that requests with a bad API key are rejected."""
    response = client.get("/search/", headers={"X-API-Key": "invalid-key"})
    assert response.status_code == 401

def test_rate_limiting():
    """
    Test the custom rate limiter blocks requests after hitting the limit.
    Because the `clean_rate_limit_logs` fixture runs before this test,
    we can be 100% sure that the count starts at 0.
    """
    for i in range(5):
        response = client.get("/search/", headers=WAYNE_HEADERS)
        assert response.status_code == 200, f"Request #{i+1} failed when it should have succeeded."

    response = client.get("/search/", headers=WAYNE_HEADERS)
    assert response.status_code == 429
    assert response.json()["detail"] == "Too Many Requests"