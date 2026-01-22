"""
HTTP client for Matrix System services.

This module provides a robust, production-ready HTTP client for interacting
with Matrix-Hub, Matrix-AI, and Matrix-Guardian services.
"""

from typing import Any, Optional

import httpx
from structlog.stdlib import BoundLogger

from matrix_system.api.exceptions import (
    MatrixAPIError,
    MatrixAuthError,
    MatrixConnectionError,
    MatrixNotFoundError,
    MatrixRateLimitError,
    MatrixTimeoutError,
    MatrixValidationError,
)
from matrix_system.utils.config import Config, get_config
from matrix_system.utils.logger import get_logger


class MatrixClient:
    """
    HTTP client for Matrix System services.

    This client provides methods to interact with all Matrix System services
    including Matrix-Hub, Matrix-AI, and Matrix-Guardian with automatic retry,
    error handling, and authentication.

    Attributes:
        config: Configuration instance
        logger: Structured logger instance
        client: HTTPX client for making requests
    """

    def __init__(
        self,
        config: Optional[Config] = None,
        logger: Optional[BoundLogger] = None,
    ) -> None:
        """
        Initialize the Matrix client.

        Args:
            config: Configuration instance (uses default if not provided)
            logger: Logger instance (creates new if not provided)
        """
        self.config = config or get_config()
        self.logger = logger or get_logger(__name__)
        self.client = httpx.Client(
            timeout=self.config.timeout,
            follow_redirects=True,
        )

    def __enter__(self) -> "MatrixClient":
        """
        Enter context manager.

        Returns:
            Self for context manager usage
        """
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exit context manager and close the client.

        Args:
            exc_type: Exception type if raised
            exc_val: Exception value if raised
            exc_tb: Exception traceback if raised
        """
        self.close()

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self.client.close()
        self.logger.debug("http_client_closed")

    def _get_headers(self) -> dict[str, str]:
        """
        Get HTTP headers for requests.

        Returns:
            Dictionary of HTTP headers including authentication if configured

        Raises:
            MatrixAuthError: If API token is required but not configured
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "matrix-system/1.0.0",
        }

        if self.config.api_token:
            headers["Authorization"] = f"Bearer {self.config.api_token}"

        return headers

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """
        Handle HTTP response and raise appropriate exceptions.

        Args:
            response: HTTP response object

        Returns:
            Parsed JSON response data

        Raises:
            MatrixAuthError: For 401/403 status codes
            MatrixNotFoundError: For 404 status code
            MatrixValidationError: For 422 status code
            MatrixRateLimitError: For 429 status code
            MatrixAPIError: For other error status codes
        """
        try:
            response.raise_for_status()
            return response.json() if response.content else {}
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            try:
                error_data = e.response.json()
                error_message = error_data.get("detail", str(e))
            except Exception:
                error_message = str(e)

            self.logger.error(
                "http_error",
                status_code=status_code,
                message=error_message,
                url=str(e.request.url),
            )

            if status_code in (401, 403):
                # Helpful hint when Matrix-Hub admin endpoints are protected
                hint = ""
                if not self.config.api_token:
                    hint = (
                        " (token missing: set MATRIX_HUB_TOKEN / MATRIX_TOKEN / API_TOKEN "
                        "for operator/admin endpoints like install/remotes/ingest)"
                    )
                raise MatrixAuthError(f"{error_message}{hint}", status_code) from e
            elif status_code == 404:
                raise MatrixNotFoundError(error_message, status_code) from e
            elif status_code == 422:
                raise MatrixValidationError(
                    error_message, status_code, error_data
                ) from e
            elif status_code == 429:
                retry_after = e.response.headers.get("Retry-After")
                raise MatrixRateLimitError(
                    error_message,
                    status_code,
                    int(retry_after) if retry_after else None,
                ) from e
            else:
                raise MatrixAPIError(error_message, status_code, error_data) from e

    def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Make an HTTP request with automatic retry and error handling.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            url: Full URL to request
            **kwargs: Additional arguments to pass to httpx.request

        Returns:
            Parsed JSON response data

        Raises:
            MatrixConnectionError: If connection fails
            MatrixTimeoutError: If request times out
            MatrixAPIError: For other API errors
        """
        headers = kwargs.pop("headers", {})
        headers.update(self._get_headers())

        self.logger.debug(
            "http_request",
            method=method,
            url=url,
            headers={k: v for k, v in headers.items() if k != "Authorization"},
        )

        retries = 0
        last_exception: Optional[Exception] = None

        while retries <= self.config.max_retries:
            try:
                response = self.client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    **kwargs,
                )
                return self._handle_response(response)

            except httpx.ConnectError as e:
                last_exception = e
                self.logger.warning(
                    "connection_error",
                    url=url,
                    attempt=retries + 1,
                    max_retries=self.config.max_retries,
                )
                retries += 1
                if retries > self.config.max_retries:
                    raise MatrixConnectionError(
                        f"Failed to connect to {url} after {retries} attempts"
                    ) from e

            except httpx.TimeoutException as e:
                last_exception = e
                self.logger.warning(
                    "timeout_error",
                    url=url,
                    timeout=self.config.timeout,
                    attempt=retries + 1,
                )
                retries += 1
                if retries > self.config.max_retries:
                    raise MatrixTimeoutError(
                        f"Request to {url} timed out after {self.config.timeout}s"
                    ) from e

            except (MatrixAuthError, MatrixValidationError, MatrixNotFoundError):
                # Don't retry for client errors
                raise

            except MatrixRateLimitError as e:
                if e.retry_after:
                    self.logger.warning(
                        "rate_limited",
                        retry_after=e.retry_after,
                        url=url,
                    )
                raise

        if last_exception:
            raise MatrixConnectionError(
                f"Failed to connect to {url} after {retries} attempts"
            ) from last_exception

        return {}

    def get(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """
        Make a GET request.

        Args:
            url: URL to request
            **kwargs: Additional arguments

        Returns:
            Parsed JSON response
        """
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """
        Make a POST request.

        Args:
            url: URL to request
            **kwargs: Additional arguments

        Returns:
            Parsed JSON response
        """
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """
        Make a PUT request.

        Args:
            url: URL to request
            **kwargs: Additional arguments

        Returns:
            Parsed JSON response
        """
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """
        Make a DELETE request.

        Args:
            url: URL to request
            **kwargs: Additional arguments

        Returns:
            Parsed JSON response
        """
        return self.request("DELETE", url, **kwargs)

    def health_check(self, service: str = "hub") -> dict[str, Any]:
        """
        Check health of a Matrix service.

        Args:
            service: Service to check ('hub', 'ai', or 'guardian')

        Returns:
            Health check response

        Raises:
            ValueError: If invalid service name provided
        """
        service_urls = {
            "hub": str(self.config.matrix_hub_url),
            "ai": str(self.config.matrix_ai_url),
            "guardian": str(self.config.matrix_guardian_url),
        }

        if service not in service_urls:
            raise ValueError(
                f"Invalid service: {service}. Must be one of {list(service_urls.keys())}"
            )

        url = f"{service_urls[service]}/health"
        return self.get(url)
