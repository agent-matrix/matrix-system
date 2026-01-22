"""
Health check and status models for Matrix System.

This module defines Pydantic models for health checks, scores,
and status tracking across Matrix System entities.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import ConfigDict, BaseModel, Field, field_validator


class HealthStatus(str, Enum):
    """
    Health status enumeration for Matrix entities.

    Attributes:
        HEALTHY: Entity is functioning normally
        DEGRADED: Entity is functioning but with reduced performance
        UNHEALTHY: Entity is not functioning properly
        UNKNOWN: Entity health status cannot be determined
    """

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class HealthCheck(BaseModel):
    """
    Health check model representing a single health assessment.

    This model captures the results of a health probe or check
    performed on a Matrix System entity.

    Attributes:
        app_uid: Unique identifier for the application/entity
        check_type: Type of health check performed
        result: Result of the check (pass/fail/warning)
        latency_ms: Response latency in milliseconds
        status: Overall health status
        score: Numeric health score (0-100)
        reasons: Additional context about the health status
        timestamp: When the check was performed
        last_checked: When the entity was last checked
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "app_uid": "app-123",
                "check_type": "http",
                "result": "pass",
                "latency_ms": 45.2,
                "status": "healthy",
                "score": 95.5,
                "reasons": {"message": "All checks passed"},
                "timestamp": "2025-01-15T10:30:00Z",
                "last_checked": "2025-01-15T10:30:00Z",
            }
        }
    )

    app_uid: str = Field(
        ...,
        description="Unique identifier for the application",
        min_length=1,
        max_length=255,
    )
    check_type: str = Field(
        ...,
        description="Type of health check (http, mcp_echo, etc.)",
        min_length=1,
    )
    result: str = Field(
        ...,
        description="Check result (pass, fail, warning)",
        pattern="^(pass|fail|warning)$",
    )
    latency_ms: Optional[float] = Field(
        default=None,
        description="Response latency in milliseconds",
        ge=0,
    )
    status: HealthStatus = Field(
        default=HealthStatus.UNKNOWN,
        description="Overall health status",
    )
    score: float = Field(
        default=0.0,
        description="Numeric health score (0-100)",
        ge=0.0,
        le=100.0,
    )
    reasons: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context about health status",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the check was performed",
    )
    last_checked: Optional[datetime] = Field(
        default=None,
        description="When the entity was last checked",
    )

    @field_validator("score")
    @classmethod
    def validate_score(cls, v: float) -> float:
        """
        Validate and normalize the health score.

        Args:
            v: Health score value

        Returns:
            Validated health score rounded to 2 decimal places
        """
        return round(v, 2)

    def is_healthy(self) -> bool:
        """
        Check if the entity is healthy.

        Returns:
            True if status is HEALTHY, False otherwise
        """
        return self.status == HealthStatus.HEALTHY

    def is_degraded(self) -> bool:
        """
        Check if the entity is degraded.

        Returns:
            True if status is DEGRADED, False otherwise
        """
        return self.status == HealthStatus.DEGRADED

    def is_unhealthy(self) -> bool:
        """
        Check if the entity is unhealthy.

        Returns:
            True if status is UNHEALTHY, False otherwise
        """
        return self.status == HealthStatus.UNHEALTHY


class HealthSummary(BaseModel):
    """
    Summary of health across multiple entities.

    Attributes:
        total_entities: Total number of entities monitored
        healthy_count: Number of healthy entities
        degraded_count: Number of degraded entities
        unhealthy_count: Number of unhealthy entities
        unknown_count: Number of entities with unknown status
        average_score: Average health score across all entities
        last_updated: When this summary was last updated
    """

    total_entities: int = Field(
        default=0,
        description="Total number of entities",
        ge=0,
    )
    healthy_count: int = Field(
        default=0,
        description="Number of healthy entities",
        ge=0,
    )
    degraded_count: int = Field(
        default=0,
        description="Number of degraded entities",
        ge=0,
    )
    unhealthy_count: int = Field(
        default=0,
        description="Number of unhealthy entities",
        ge=0,
    )
    unknown_count: int = Field(
        default=0,
        description="Number of entities with unknown status",
        ge=0,
    )
    average_score: float = Field(
        default=0.0,
        description="Average health score",
        ge=0.0,
        le=100.0,
    )
    last_updated: datetime = Field(
        default_factory=datetime.utcnow,
        description="When summary was last updated",
    )

    def health_percentage(self) -> float:
        """
        Calculate percentage of healthy entities.

        Returns:
            Percentage of healthy entities (0-100)
        """
        if self.total_entities == 0:
            return 0.0
        return round((self.healthy_count / self.total_entities) * 100, 2)
