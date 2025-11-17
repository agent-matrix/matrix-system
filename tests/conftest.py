"""Pytest configuration and fixtures for Matrix System tests."""

import pytest

from matrix_system.utils.config import Config


@pytest.fixture
def test_config() -> Config:
    """
    Create a test configuration instance.

    Returns:
        Config instance with test values
    """
    return Config(
        matrix_hub_url="http://localhost:8000",
        matrix_ai_url="http://localhost:7860",
        matrix_guardian_url="http://localhost:8080",
        timeout=10,
        max_retries=1,
        log_level="DEBUG",
    )


@pytest.fixture
def sample_app_uid() -> str:
    """
    Provide a sample application UID for testing.

    Returns:
        Sample application UID
    """
    return "test-app-123"
