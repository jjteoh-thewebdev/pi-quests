import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

# Create test client
client = TestClient(app)

# Set test API key for authentication
TEST_API_KEY = "test_api_key"

# Mock environment variables
@pytest.fixture(autouse=True)
def mock_env_variables():
    with patch.dict(os.environ, {"API_KEY": TEST_API_KEY}):
        yield

# Mock Redis repository responses
@pytest.fixture
def mock_redis_repository():
    with patch("app.infrastructure.redis_repository.RedisRepository") as mock:
        instance = mock.return_value
        instance.get_cached_pi.return_value = ("3.14159265358979323846", 20)
        yield instance

# Mock Pi service
@pytest.fixture
def mock_pi_service(mock_redis_repository):
    with patch("app.application.pi_service.PiService") as mock:
        instance = mock.return_value
        instance.get_current_pi.return_value = ("3.14159265358979323846", 20)
        yield instance

def test_get_pi_with_valid_api_key(mock_pi_service):
    """Test retrieving Pi with a valid API key."""
    response = client.get("/api/pi", headers={"x-api-key": TEST_API_KEY})
    
    assert response.status_code == 200
    data = response.json()
    assert "pi" in data
    assert "dp" in data
    assert data["pi"] == "3.14159265358979323846"
    assert data["dp"] == "20"

def test_get_pi_with_invalid_api_key(mock_pi_service):
    """Test retrieving Pi with an invalid API key."""
    response = client.get("/api/pi", headers={"x-api-key": "invalid_key"})
    
    assert response.status_code == 401

def test_get_pi_without_api_key(mock_pi_service):
    """Test retrieving Pi without an API key."""
    response = client.get("/api/pi")
    
    assert response.status_code == 422  # Unprocessable Entity (missing required header)

def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy" 