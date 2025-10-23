"""
Test module for the activities endpoints.
"""
import pytest
from fastapi.testclient import TestClient

def test_root_redirect(client: TestClient):
    """Test that the root endpoint redirects to the static index.html."""
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    if response.status_code == 307:
        assert response.headers["location"] == "/static/index.html"

def test_get_activities(client: TestClient):
    """Test getting the list of activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    # Check activity structure
    for activity in data.values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

def test_signup_success(client: TestClient, valid_email):
    """Test successful activity signup."""
    activity_name = "Chess Club"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": valid_email})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert valid_email in data["message"]
    assert activity_name in data["message"]

def test_signup_invalid_email(client: TestClient, invalid_email):
    """Test signup with invalid email domain."""
    response = client.post("/activities/Chess Club/signup", params={"email": invalid_email})
    assert response.status_code == 400
    assert "Invalid email format" in response.json()["detail"]

def test_signup_nonexistent_activity(client: TestClient, valid_email):
    """Test signup for non-existent activity."""
    response = client.post("/activities/NonexistentClub/signup", params={"email": valid_email})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_signup_duplicate(client: TestClient, valid_email):
    """Test duplicate signup attempt."""
    activity_name = "Chess Club"
    # First signup
    client.post(f"/activities/{activity_name}/signup", params={"email": valid_email})
    # Duplicate signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": valid_email})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_full_activity(client: TestClient, valid_email):
    """Test signup for full activity."""
    activity_name = "Chess Club"
    max_emails = 12  # Based on Chess Club max_participants
    
    # Fill up the activity
    test_emails = [f"test{i}@mergington.edu" for i in range(max_emails)]
    for email in test_emails:
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        if response.status_code == 400 and "already signed up" in response.json()["detail"]:
            continue
        assert response.status_code == 200

    # Try to sign up one more participant
    response = client.post(f"/activities/{activity_name}/signup", params={"email": valid_email})
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]

def test_unregister_success(client: TestClient, valid_email):
    """Test successful activity unregistration."""
    activity_name = "Chess Club"
    # First sign up
    client.post(f"/activities/{activity_name}/signup", params={"email": valid_email})
    # Then unregister
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": valid_email})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert valid_email in data["message"]
    assert activity_name in data["message"]

def test_unregister_not_registered(client: TestClient, valid_email):
    """Test unregistering when not registered."""
    response = client.post("/activities/Chess Club/unregister", params={"email": valid_email})
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

def test_unregister_invalid_email(client: TestClient, invalid_email):
    """Test unregistering with invalid email domain."""
    response = client.post("/activities/Chess Club/unregister", params={"email": invalid_email})
    assert response.status_code == 400
    assert "Invalid email format" in response.json()["detail"]

def test_case_insensitive_activity_names(client: TestClient, valid_email):
    """Test that activity names are case-insensitive."""
    variations = ["Chess Club", "chess club", "CHESS CLUB", "ChEsS cLuB"]
    
    # Try signing up with different case variations
    for name in variations:
        response = client.post(f"/activities/{name}/signup", params={"email": f"test{name}@mergington.edu"})
        assert response.status_code == 200
        assert "Chess Club" in response.json()["message"]  # Should always return canonical name