import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for interscholastic games",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn and practice tennis skills with coaching",
        "schedule": "Tuesdays and Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["rachel@mergington.edu"]
    },
    "Art Studio": {
        "description": "Express creativity through painting, drawing, and sculpture",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["jessica@mergington.edu", "carlos@mergington.edu"]
    },
    "Music Band": {
        "description": "Play musical instruments and perform in school concerts",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["anna@mergington.edu", "thomas@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore scientific experiments and research projects",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["sarah@mergington.edu", "matthew@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(INITIAL_ACTIVITIES)

client = TestClient(app)

def test_get_activities():
    # Arrange - handled by fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert len(data["Chess Club"]["participants"]) == 2
    expected_activities = ["Chess Club", "Programming Class", "Gym Class", "Basketball Team", "Tennis Club", "Art Studio", "Music Band", "Debate Team", "Science Club"]
    assert set(data.keys()) == set(expected_activities)

def test_signup_success():
    # Arrange
    new_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess%20Club/signup?email={new_email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    # Verify added
    response = client.get("/activities")
    data = response.json()
    assert new_email in data["Chess Club"]["participants"]

def test_signup_duplicate():
    # Arrange
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess%20Club/signup?email={existing_email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]

def test_signup_activity_not_found():
    # Arrange

    # Act
    response = client.post("/activities/NonExistent/signup?email=test@test.com")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_remove_participant_success():
    # Arrange
    email_to_remove = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess%20Club/participants?email={email_to_remove}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Removed" in result["message"]
    # Verify removed
    response = client.get("/activities")
    data = response.json()
    assert email_to_remove not in data["Chess Club"]["participants"]

def test_remove_participant_not_found():
    # Arrange

    # Act
    response = client.delete("/activities/Chess%20Club/participants?email=nonexistent@test.com")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Participant not found" in result["detail"]

def test_remove_activity_not_found():
    # Arrange

    # Act
    response = client.delete("/activities/NonExistent/participants?email=test@test.com")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]