import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

# Create test client
client = TestClient(app)

# Set test API key for authentication
TEST_API_KEY = "your_api_key_here"

mockedPiValue = "3.14159265358979323846"

# Mock environment variables
@pytest.fixture(autouse=True)
def mock_env_variables():
    with patch.dict(os.environ, {"API_KEY": TEST_API_KEY}):
        yield


# Mock Pi service - patch the SINGLETON instance returned by get_pi_service
@pytest.fixture
def mock_pi_service():
    mock_instance = MagicMock()
    mock_instance.get_current_pi.return_value = (mockedPiValue, len(mockedPiValue) - 2)
    
    with patch("app.api.dependencies.pi_service", mock_instance), \
         patch("app.api.dependencies.get_pi_service", return_value=mock_instance):
        yield mock_instance

def test_get_pi_with_valid_api_key(mock_pi_service):
    """Test retrieving Pi with a valid API key."""
    response = client.get("/api/pi", headers={"x-api-key": TEST_API_KEY})
    
    # Check response status
    assert response.status_code == 200
    
    # Check response data structure
    data = response.json()
    assert "pi" in data
    assert "dp" in data
    
    # Check the first 10 digits of the response values
    assert data["pi"].startswith(mockedPiValue[:10])

def test_get_pi_with_invalid_api_key():
    """Test retrieving Pi with an invalid API key."""
    response = client.get("/api/pi", headers={"x-api-key": "invalid_key"})
    
    assert response.status_code == 401

def test_get_pi_without_api_key():
    """Test retrieving Pi without an API key."""
    response = client.get("/api/pi")
    
    assert response.status_code == 401 

def test_get_pi_service_unavailable(mock_pi_service):
    """Test when Pi service returns None (calculation in progress)."""
    # Mock service to return None, indicating calculation in progress
    mock_pi_service.get_current_pi.return_value = (None, None)
    
    response = client.get("/api/pi", headers={"x-api-key": TEST_API_KEY})
    
    assert response.status_code == 503
    data = response.json()
    assert "detail" in data
    assert "not available" in data["detail"] 