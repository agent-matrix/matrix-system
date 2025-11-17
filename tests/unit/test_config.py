"""Unit tests for configuration module."""

import pytest
from pydantic import ValidationError

from matrix_system.utils.config import Config


class TestConfig:
    """Test cases for Config class."""

    def test_default_config(self) -> None:
        """Test that default configuration loads successfully."""
        config = Config()
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.log_level == "INFO"
        assert config.log_json is False

    def test_custom_timeout(self) -> None:
        """Test custom timeout configuration."""
        config = Config(timeout=60)
        assert config.timeout == 60

    def test_invalid_timeout(self) -> None:
        """Test that invalid timeout raises validation error."""
        with pytest.raises(ValidationError):
            Config(timeout=0)

        with pytest.raises(ValidationError):
            Config(timeout=500)

    def test_log_level_validation(self) -> None:
        """Test log level validation."""
        config = Config(log_level="debug")
        assert config.log_level == "DEBUG"

        with pytest.raises(ValidationError):
            Config(log_level="INVALID")

    def test_api_token_optional(self) -> None:
        """Test that API token is optional."""
        config = Config()
        assert config.api_token is None

        config_with_token = Config(api_token="test-token")
        assert config_with_token.api_token == "test-token"

    def test_max_retries_bounds(self) -> None:
        """Test max_retries validation bounds."""
        config = Config(max_retries=5)
        assert config.max_retries == 5

        with pytest.raises(ValidationError):
            Config(max_retries=-1)

        with pytest.raises(ValidationError):
            Config(max_retries=20)
