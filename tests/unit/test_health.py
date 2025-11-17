"""Unit tests for health models."""

from datetime import datetime

import pytest

from matrix_system.models.health import (
    HealthCheck,
    HealthStatus,
    HealthSummary,
)


class TestHealthStatus:
    """Test cases for HealthStatus enum."""

    def test_health_status_values(self) -> None:
        """Test that all health status values are defined."""
        assert HealthStatus.HEALTHY == "healthy"
        assert HealthStatus.DEGRADED == "degraded"
        assert HealthStatus.UNHEALTHY == "unhealthy"
        assert HealthStatus.UNKNOWN == "unknown"


class TestHealthCheck:
    """Test cases for HealthCheck model."""

    def test_create_health_check(self) -> None:
        """Test creating a valid health check."""
        check = HealthCheck(
            app_uid="test-app",
            check_type="http",
            result="pass",
            status=HealthStatus.HEALTHY,
            score=95.5,
        )
        assert check.app_uid == "test-app"
        assert check.check_type == "http"
        assert check.result == "pass"
        assert check.status == HealthStatus.HEALTHY
        assert check.score == 95.5

    def test_health_check_defaults(self) -> None:
        """Test default values for health check."""
        check = HealthCheck(
            app_uid="test-app",
            check_type="http",
            result="pass",
        )
        assert check.status == HealthStatus.UNKNOWN
        assert check.score == 0.0
        assert check.reasons == {}
        assert isinstance(check.timestamp, datetime)

    def test_score_validation(self) -> None:
        """Test that score is validated and normalized."""
        check = HealthCheck(
            app_uid="test-app",
            check_type="http",
            result="pass",
            score=95.555,
        )
        assert check.score == 95.56  # Rounded to 2 decimals

    def test_is_healthy(self) -> None:
        """Test is_healthy method."""
        check = HealthCheck(
            app_uid="test-app",
            check_type="http",
            result="pass",
            status=HealthStatus.HEALTHY,
        )
        assert check.is_healthy() is True
        assert check.is_degraded() is False
        assert check.is_unhealthy() is False

    def test_is_degraded(self) -> None:
        """Test is_degraded method."""
        check = HealthCheck(
            app_uid="test-app",
            check_type="http",
            result="warning",
            status=HealthStatus.DEGRADED,
        )
        assert check.is_healthy() is False
        assert check.is_degraded() is True
        assert check.is_unhealthy() is False

    def test_invalid_result(self) -> None:
        """Test that invalid result values are rejected."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            HealthCheck(
                app_uid="test-app",
                check_type="http",
                result="invalid",
            )


class TestHealthSummary:
    """Test cases for HealthSummary model."""

    def test_create_summary(self) -> None:
        """Test creating a health summary."""
        summary = HealthSummary(
            total_entities=10,
            healthy_count=8,
            degraded_count=1,
            unhealthy_count=1,
            average_score=85.5,
        )
        assert summary.total_entities == 10
        assert summary.healthy_count == 8
        assert summary.degraded_count == 1
        assert summary.unhealthy_count == 1
        assert summary.average_score == 85.5

    def test_health_percentage(self) -> None:
        """Test health percentage calculation."""
        summary = HealthSummary(
            total_entities=10,
            healthy_count=8,
        )
        assert summary.health_percentage() == 80.0

    def test_health_percentage_zero_entities(self) -> None:
        """Test health percentage with zero entities."""
        summary = HealthSummary(total_entities=0)
        assert summary.health_percentage() == 0.0
