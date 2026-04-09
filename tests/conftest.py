"""Pytest configuration and fixtures for API tests."""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities as original_activities


@pytest.fixture
def reset_activities():
    """Reset activities database before and after each test."""
    # Store original state
    original_state = {
        key: {"participants": value["participants"].copy()}
        for key, value in original_activities.items()
    }
    
    yield
    
    # Restore original state after test
    for activity_name, original_data in original_state.items():
        original_activities[activity_name]["participants"] = original_data["participants"].copy()


@pytest.fixture
def client(reset_activities):
    """Create a TestClient for the FastAPI app with fresh activities."""
    return TestClient(app)
