def test_list_routes():
    print("\nRegistered routes:")
    for route in app.routes:
        if hasattr(route, 'methods'):
            print(f"{route.path} [{','.join(route.methods)}]")
import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Drama Club" in data

def test_signup_and_unregister():
    activity = "Drama Club"
    email = "testuser@mergington.edu"
    # Ensure user is not already signed up
    client.post(f"/activities/unregister/{activity}?email={email}")
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Unregister
    response = client.post(f"/activities/unregister/{activity}?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

def test_signup_duplicate():
    activity = "Drama Club"
    email = "testuser2@mergington.edu"
    client.post(f"/activities/unregister/{activity}?email={email}")
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    client.post(f"/activities/{activity}/unregister?email={email}")

def test_signup_full():
    activity = "Math Olympiad"
    emails = [f"fulltest{i}@mergington.edu" for i in range(11)]
    # Unregister all test emails first
    for email in emails:
        client.post(f"/activities/unregister/{activity}?email={email}")
    # Fill up activity
    for email in emails[:-1]:
        client.post(f"/activities/{activity}/signup?email={email}")
    # Try to sign up one more
    response = client.post(f"/activities/{activity}/signup?email={emails[-1]}")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]
    # Cleanup
    for email in emails:
        client.post(f"/activities/{activity}/unregister?email={email}")
