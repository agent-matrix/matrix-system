"""
API client module for Matrix System.

This module provides HTTP client interfaces for interacting with
Matrix-Hub, Matrix-AI, and Matrix-Guardian services.
"""

from matrix_system.api.client import MatrixClient
from matrix_system.api.exceptions import (
    MatrixAPIError,
    MatrixAuthError,
    MatrixConnectionError,
    MatrixTimeoutError,
)

__all__ = [
    "MatrixClient",
    "MatrixAPIError",
    "MatrixAuthError",
    "MatrixConnectionError",
    "MatrixTimeoutError",
]
