"""
Tests for health check endpoint.

This module contains tests for the health check functionality,
following TDD principles - tests written before implementation.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


class TestHealthCheck:
    """Test cases for health check endpoint."""
    
    def test_health_check_returns_200(self, client: TestClient):
        """
        Test that health check endpoint returns 200 status code.
        
        Given: A FastAPI application is running
        When: A GET request is made to /health
        Then: The response should have status code 200
        """
        # Arrange
        endpoint = "/health"
        
        # Act
        response = client.get(endpoint)
        
        # Assert
        assert response.status_code == 200
    
    def test_health_check_returns_json(self, client: TestClient):
        """
        Test that health check endpoint returns JSON response.
        
        Given: A FastAPI application is running
        When: A GET request is made to /health
        Then: The response should be valid JSON
        """
        # Arrange
        endpoint = "/health"
        
        # Act
        response = client.get(endpoint)
        
        # Assert
        assert response.headers["content-type"] == "application/json"
    
    def test_health_check_returns_expected_structure(self, client: TestClient):
        """
        Test that health check endpoint returns expected response structure.
        
        Given: A FastAPI application is running
        When: A GET request is made to /health
        Then: The response should contain status and timestamp
        """
        # Arrange
        endpoint = "/health"
        
        # Act
        response = client.get(endpoint)
        
        # Assert
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert data["status"] == "healthy"
    
    def test_health_check_includes_version(self, client: TestClient):
        """
        Test that health check endpoint includes application version.
        
        Given: A FastAPI application is running
        When: A GET request is made to /health
        Then: The response should include version information
        """
        # Arrange
        endpoint = "/health"
        
        # Act
        response = client.get(endpoint)
        
        # Assert
        data = response.json()
        assert "version" in data
        assert isinstance(data["version"], str)
    
    def test_health_check_includes_environment(self, client: TestClient):
        """
        Test that health check endpoint includes environment information.
        
        Given: A FastAPI application is running
        When: A GET request is made to /health
        Then: The response should include environment information
        """
        # Arrange
        endpoint = "/health"
        
        # Act
        response = client.get(endpoint)
        
        # Assert
        data = response.json()
        assert "environment" in data
        assert data["environment"] in ["development", "staging", "production"]


@pytest.fixture
def client():
    """
    Fixture to create a test client for FastAPI application.
    
    Returns:
        TestClient: A test client instance for making requests
    """
    from app.main import app
    return TestClient(app)
