"""
Event models for Matrix System audit trail.

This module defines Pydantic models for events that are logged
to the append-only audit trail in the Matrix System.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """
    Event type enumeration for audit trail.

    Attributes:
        HEALTH_UPDATE: Health status was updated
        PLAN_CREATED: AI plan was created
        PLAN_APPROVED: Plan was approved by operator
        PLAN_REJECTED: Plan was rejected by operator
        PLAN_EXECUTED: Plan was executed
        AUTOPILOT_ACTION: Autopilot performed an action
        ERROR_DETECTED: Error was detected
        RECOVERY_STARTED: Recovery process started
        RECOVERY_COMPLETED: Recovery process completed
        SYSTEM_STARTUP: System started up
        SYSTEM_SHUTDOWN: System shut down
    """

    HEALTH_UPDATE = "health.update"
    PLAN_CREATED = "guardian.plan"
    PLAN_APPROVED = "guardian.approve"
    PLAN_REJECTED = "guardian.reject"
    PLAN_EXECUTED = "guardian.execute"
    AUTOPILOT_ACTION = "autopilot.action"
    ERROR_DETECTED = "error.detected"
    RECOVERY_STARTED = "recovery.started"
    RECOVERY_COMPLETED = "recovery.completed"
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown"


class Event(BaseModel):
    """
    Event model for audit trail entries.

    This model represents a single event in the append-only audit log,
    capturing all actions and state changes in the Matrix System.

    Attributes:
        id: Unique event identifier (assigned by database)
        event_type: Type of event
        app_uid: Application/entity identifier if applicable
        payload: Event-specific data
        actor: Who or what triggered the event
        timestamp: When the event occurred
        metadata: Additional metadata about the event
    """

    id: Optional[int] = Field(
        default=None,
        description="Unique event identifier",
    )
    event_type: EventType = Field(
        ...,
        description="Type of event",
    )
    app_uid: Optional[str] = Field(
        default=None,
        description="Application identifier if applicable",
        max_length=255,
    )
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Event-specific data",
    )
    actor: str = Field(
        default="system",
        description="Who or what triggered the event",
        max_length=255,
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the event occurred",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional event metadata",
    )

    def is_critical(self) -> bool:
        """
        Check if this is a critical event.

        Returns:
            True if event type indicates critical situation
        """
        critical_types = {
            EventType.ERROR_DETECTED,
            EventType.PLAN_REJECTED,
            EventType.SYSTEM_SHUTDOWN,
        }
        return self.event_type in critical_types

    def is_success(self) -> bool:
        """
        Check if this is a success event.

        Returns:
            True if event type indicates successful operation
        """
        success_types = {
            EventType.PLAN_APPROVED,
            EventType.PLAN_EXECUTED,
            EventType.RECOVERY_COMPLETED,
            EventType.AUTOPILOT_ACTION,
        }
        return self.event_type in success_types

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "id": 12345,
                "event_type": "guardian.plan",
                "app_uid": "app-123",
                "payload": {
                    "plan": {
                        "action": "pin_lkg",
                        "version": "1.2.3",
                    }
                },
                "actor": "matrix-guardian",
                "timestamp": "2025-01-15T10:30:00Z",
                "metadata": {
                    "source": "health_monitor",
                    "severity": "low",
                },
            }
        }


class EventFilter(BaseModel):
    """
    Filter criteria for querying events.

    Attributes:
        event_types: Filter by event types
        app_uid: Filter by application identifier
        actor: Filter by actor
        start_time: Filter events after this time
        end_time: Filter events before this time
        limit: Maximum number of events to return
        offset: Number of events to skip
    """

    event_types: Optional[list[EventType]] = Field(
        default=None,
        description="Filter by event types",
    )
    app_uid: Optional[str] = Field(
        default=None,
        description="Filter by application identifier",
    )
    actor: Optional[str] = Field(
        default=None,
        description="Filter by actor",
    )
    start_time: Optional[datetime] = Field(
        default=None,
        description="Filter events after this time",
    )
    end_time: Optional[datetime] = Field(
        default=None,
        description="Filter events before this time",
    )
    limit: int = Field(
        default=100,
        description="Maximum events to return",
        ge=1,
        le=1000,
    )
    offset: int = Field(
        default=0,
        description="Number of events to skip",
        ge=0,
    )
