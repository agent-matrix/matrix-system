"""
Exception classes for Matrix System API client.

This module defines custom exceptions for handling various error
scenarios when interacting with Matrix System services.
"""

from typing import Any, Optional


class MatrixAPIError(Exception):
    """
    Base exception for all Matrix API errors.

    Attributes:
        message: Error message describing what went wrong
        status_code: HTTP status code if applicable
        response_data: Additional response data from the API
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Initialize the Matrix API error.

        Args:
            message: Error message
            status_code: HTTP status code
            response_data: Additional response data
        """
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        Return string representation of the error.

        Returns:
            Formatted error message with status code if available
        """
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class MatrixConnectionError(MatrixAPIError):
    """
    Exception raised when connection to Matrix services fails.

    This exception is raised when the client cannot establish a connection
    to any Matrix service due to network issues or service unavailability.
    """

    def __init__(self, message: str = "Failed to connect to Matrix service") -> None:
        """
        Initialize the connection error.

        Args:
            message: Error message describing the connection failure
        """
        super().__init__(message)


class MatrixTimeoutError(MatrixAPIError):
    """
    Exception raised when a request to Matrix services times out.

    This exception is raised when a request exceeds the configured timeout
    duration without receiving a response.
    """

    def __init__(self, message: str = "Request to Matrix service timed out") -> None:
        """
        Initialize the timeout error.

        Args:
            message: Error message describing the timeout
        """
        super().__init__(message)


class MatrixAuthError(MatrixAPIError):
    """
    Exception raised when authentication fails.

    This exception is raised when the provided API token is invalid,
    expired, or missing when required.
    """

    def __init__(
        self,
        message: str = "Authentication failed",
        status_code: int = 401,
    ) -> None:
        """
        Initialize the authentication error.

        Args:
            message: Error message describing the authentication failure
            status_code: HTTP status code (typically 401 or 403)
        """
        super().__init__(message, status_code)


class MatrixValidationError(MatrixAPIError):
    """
    Exception raised when request validation fails.

    This exception is raised when the request data does not meet
    the API's validation requirements.
    """

    def __init__(
        self,
        message: str = "Request validation failed",
        status_code: int = 422,
        response_data: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Initialize the validation error.

        Args:
            message: Error message describing the validation failure
            status_code: HTTP status code (typically 422)
            response_data: Validation error details from the API
        """
        super().__init__(message, status_code, response_data)


class MatrixNotFoundError(MatrixAPIError):
    """
    Exception raised when a requested resource is not found.

    This exception is raised when attempting to access a resource
    that does not exist in the Matrix system.
    """

    def __init__(
        self,
        message: str = "Resource not found",
        status_code: int = 404,
    ) -> None:
        """
        Initialize the not found error.

        Args:
            message: Error message describing what was not found
            status_code: HTTP status code (typically 404)
        """
        super().__init__(message, status_code)


class MatrixRateLimitError(MatrixAPIError):
    """
    Exception raised when rate limit is exceeded.

    This exception is raised when too many requests are made to
    the Matrix services in a short period of time.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        status_code: int = 429,
        retry_after: Optional[int] = None,
    ) -> None:
        """
        Initialize the rate limit error.

        Args:
            message: Error message describing the rate limit
            status_code: HTTP status code (typically 429)
            retry_after: Number of seconds to wait before retrying
        """
        self.retry_after = retry_after
        super().__init__(message, status_code)
