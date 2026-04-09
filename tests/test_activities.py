"""
Tests for Mergington High School Activities API.

Uses the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and preconditions
- Act: Execute the API request
- Assert: Verify response status, data, and side effects
"""
import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_all_activities_returns_200(self, client):
        """Arrange: No setup needed. Act: Request all activities. Assert: Status 200."""
        # Arrange
        # (no setup needed)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_activities_returns_all_activities(self, client):
        """Arrange: Know default activities. Act: Get activities. Assert: All returned."""
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer",
            "Basketball",
            "Art Club",
            "Drama",
            "Debate Club",
            "Math Olympiad"
        ]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert len(data) == len(expected_activities)
        for activity_name in expected_activities:
            assert activity_name in data
    
    def test_activity_has_required_fields(self, client):
        """Arrange: Know activity structure. Act: Get activities. Assert: All fields present."""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity in data.values():
            for field in required_fields:
                assert field in activity
    
    def test_participants_is_list(self, client):
        """Arrange: Know participants should be list. Act: Get activities. Assert: Verified."""
        # Arrange
        # (no setup needed)
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity in data.values():
            assert isinstance(activity["participants"], list)


class TestRootRedirect:
    """Tests for GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """Arrange: No setup. Act: Request root. Assert: Redirects to /static/index.html."""
        # Arrange
        # (no setup needed)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_new_student_returns_200(self, client):
        """Arrange: New student, activity available. Act: Sign up. Assert: Status 200."""
        # Arrange
        activity_name = "Soccer"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_signup_adds_participant_to_activity(self, client):
        """Arrange: New student, activity available. Act: Sign up. Assert: Participant added."""
        # Arrange
        activity_name = "Soccer"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
    
    def test_signup_returns_success_message(self, client):
        """Arrange: New student, activity available. Act: Sign up. Assert: Message returned."""
        # Arrange
        activity_name = "Soccer"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """Arrange: Activity doesn't exist. Act: Try to sign up. Assert: Status 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_duplicate_student_returns_400(self, client):
        """Arrange: Student already signed up. Act: Try to sign up again. Assert: Status 400."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up to Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"
    
    def test_signup_same_student_different_activities(self, client):
        """Arrange: Student in one activity. Act: Sign up for another. Assert: Success."""
        # Arrange
        student_email = "newstudent@mergington.edu"
        activity1 = "Soccer"
        activity2 = "Basketball"
        
        # Act - Sign up for first activity
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": student_email}
        )
        
        # Act - Sign up for second activity
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify in both activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert student_email in activities[activity1]["participants"]
        assert student_email in activities[activity2]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""
    
    def test_unregister_existing_participant_returns_200(self, client):
        """Arrange: Student signed up. Act: Unregister. Assert: Status 200."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_unregister_removes_participant_from_activity(self, client):
        """Arrange: Student signed up. Act: Unregister. Assert: Participant removed."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]
    
    def test_unregister_returns_success_message(self, client):
        """Arrange: Student signed up. Act: Unregister. Assert: Message returned."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Arrange: Activity doesn't exist. Act: Try to unregister. Assert: Status 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_non_participant_returns_400(self, client):
        """Arrange: Student not signed up. Act: Try to unregister. Assert: Status 400."""
        # Arrange
        activity_name = "Soccer"
        email = "notasignedupstudent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student not signed up for this activity"
    
    def test_unregister_then_signup_again(self, client):
        """Arrange: Student signed up. Act: Unregister then sign up. Assert: Both succeed."""
        # Arrange
        activity_name = "Soccer"
        email = "student@mergington.edu"
        
        # Act - Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act - Sign up again
        signup_again_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert signup_response.status_code == 200
        assert unregister_response.status_code == 200
        assert signup_again_response.status_code == 200
