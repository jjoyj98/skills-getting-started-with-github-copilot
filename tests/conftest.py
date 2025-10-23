import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def valid_activity():
    """Return a valid activity for testing."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        }
    }

@pytest.fixture
def valid_email():
    """Return a valid email for testing."""
    return "test@mergington.edu"

@pytest.fixture
def invalid_email():
    """Return an invalid email for testing."""
    return "test@example.com"