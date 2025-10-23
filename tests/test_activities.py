from fastapi.testclient import TestClient
import pytest

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Make a shallow copy of participants to restore after each test
    original = {k: v["participants"][:] for k, v in activities.items()}
    yield
    for k, v in original.items():
        activities[k]["participants"] = v[:]


def test_get_activities_returns_200_and_payload():
    client = TestClient(app)

    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_prevent_duplicate_signup():
    client = TestClient(app)
    activity = "Chess Club"
    email = "test_student@example.com"

    # Sign up successfully
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should return 400
    resp2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp2.status_code == 400


def test_unregister_participant():
    client = TestClient(app)
    activity = "Programming Class"
    email = "temp_student@example.com"

    # Ensure student is signed up first
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Unregister
    resp2 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp2.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should fail with 400
    resp3 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp3.status_code == 400
