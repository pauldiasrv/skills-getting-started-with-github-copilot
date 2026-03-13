from urllib.parse import quote

import src.app as app_module


def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup?email={email}")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup?email={email}")
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup?email={email}")
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up"


def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/participants?email={email}")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/participants?email={email}")
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_404_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity}/participants?email={email}")
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found in this activity"


def test_signup_then_unregister_updates_participant_count(client):
    # Arrange
    activity_name = "Chess Club"
    email = "state.check@mergington.edu"
    encoded_activity = quote(activity_name, safe="")
    initial_count = len(app_module.activities[activity_name]["participants"])

    # Act
    signup_response = client.post(f"/activities/{encoded_activity}/signup?email={email}")
    post_signup_count = len(app_module.activities[activity_name]["participants"])
    unregister_response = client.delete(f"/activities/{encoded_activity}/participants?email={email}")
    final_count = len(app_module.activities[activity_name]["participants"])

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert post_signup_count == initial_count + 1
    assert final_count == initial_count
    assert email not in app_module.activities[activity_name]["participants"]
