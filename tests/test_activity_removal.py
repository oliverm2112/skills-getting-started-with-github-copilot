import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


def test_remove_participant_from_activity(client):
    activity_name = "Chess Club"
    email = "remove-test@mergington.edu"
    participants = activities[activity_name]["participants"]
    participants.append(email)

    try:
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        assert response.status_code == 200
        assert response.json() == {"message": f"Removed {email} from {activity_name}"}
        assert email not in participants
    finally:
        if email in participants:
            participants.remove(email)


def test_remove_participant_returns_not_found_when_not_signed_up(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "not-signed-up@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_remove_participant_returns_not_found_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
