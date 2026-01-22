"""
Configuration management for Matrix System.

This module provides configuration loading and validation using
Pydantic settings with support for environment variables and .env files.
"""

from typing import Optional

from pydantic import AliasChoices, Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Application configuration with environment variable support.

    This class loads configuration from environment variables and .env files,
    providing type validation and default values for all Matrix System settings.

    Attributes:
        matrix_hub_url: Base URL for Matrix-Hub API
        matrix_ai_url: Base URL for Matrix-AI service
        matrix_guardian_url: Base URL for Matrix-Guardian service
        api_token: Bearer token for API authentication
        timeout: HTTP request timeout in seconds
        max_retries: Maximum number of retry attempts for failed requests
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_json: Enable JSON format for logs
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,  # Allow both field name and aliases
    )

    # API Endpoints
    matrix_hub_url: HttpUrl = Field(
        default="https://api.matrixhub.io",
        description="Base URL for Matrix-Hub API",
    )
    matrix_ai_url: HttpUrl = Field(
        default="https://huggingface.co/spaces/agent-matrix/matrix-ai",
        description="Base URL for Matrix-AI service",
    )
    matrix_guardian_url: HttpUrl = Field(
        default="http://localhost:8080",
        description="Base URL for Matrix-Guardian service",
    )

    # Authentication
    api_token: Optional[str] = Field(
        default=None,
        description="Bearer token for API authentication",
        validation_alias=AliasChoices(
            "MATRIX_HUB_TOKEN",  # preferred in ecosystem/CLI
            "MATRIX_TOKEN",      # fallback alias
            "API_TOKEN",         # backward-compatible
        ),
    )

    # HTTP Configuration
    timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="HTTP request timeout in seconds",
    )
    max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum number of retry attempts",
    )

    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level",
    )
    log_json: bool = Field(
        default=False,
        description="Enable JSON format for logs",
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """
        Validate that the log level is valid.

        Args:
            v: Log level string to validate

        Returns:
            Validated log level in uppercase

        Raises:
            ValueError: If the log level is invalid
        """
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(
                f"Invalid log level: {v}. Must be one of {', '.join(valid_levels)}"
            )
        return v_upper


_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance (singleton pattern).

    Returns:
        Global Config instance

    Example:
        >>> config = get_config()
        >>> print(config.matrix_hub_url)
        https://api.matrixhub.io
    """
    global _config
    if _config is None:
        _config = Config()
    return _config
