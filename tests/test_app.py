import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Chess%20Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_duplicate():
    # First signup
    client.post("/activities/Drama%20Club/signup?email=dupe@mergington.edu")
    # Duplicate signup
    response = client.post("/activities/Drama%20Club/signup?email=dupe@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_full():
    # Get current state from API
    resp = client.get("/activities")
    data = resp.json()
    max_participants = data["Math Olympiad"]["max_participants"]
    current_count = len(data["Math Olympiad"]["participants"])
    # Fill up the activity
    for i in range(max_participants - current_count):
        client.post(f"/activities/Math%20Olympiad/signup?email=full{i}@mergington.edu")
    # Try to add one more
    response = client.post("/activities/Math%20Olympiad/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]
