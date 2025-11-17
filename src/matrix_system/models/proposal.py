"""
Proposal models for Matrix System decision workflow.

This module defines Pydantic models for AI-generated proposals
and their approval workflow in the Matrix System.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ProposalState(str, Enum):
    """
    Proposal state enumeration.

    Attributes:
        PENDING: Proposal is awaiting review
        APPROVED: Proposal has been approved
        REJECTED: Proposal has been rejected
        EXECUTING: Proposal is being executed
        COMPLETED: Proposal execution completed
        FAILED: Proposal execution failed
        CANCELLED: Proposal was cancelled
    """

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProposalType(str, Enum):
    """
    Proposal type enumeration.

    Attributes:
        LKG_PIN: Pin to last known good version
        VERSION_ROLLBACK: Rollback to previous version
        CACHE_WARMUP: Warm up cache
        METADATA_FIX: Fix metadata issues
        BUNDLE_MIRROR: Mirror bundle to CAS
        CUSTOM: Custom proposal type
    """

    LKG_PIN = "lkg_pin"
    VERSION_ROLLBACK = "version_rollback"
    CACHE_WARMUP = "cache_warmup"
    METADATA_FIX = "metadata_fix"
    BUNDLE_MIRROR = "bundle_mirror"
    CUSTOM = "custom"


class Proposal(BaseModel):
    """
    Proposal model for AI-generated remediation plans.

    This model represents a proposed action or set of actions
    to address issues detected in the Matrix System.

    Attributes:
        id: Unique proposal identifier
        app_uid: Application identifier
        proposal_type: Type of proposal
        state: Current state of the proposal
        diff: Changes to be made
        rationale: Explanation of why this proposal was created
        risk_score: Risk assessment score (0-100, lower is safer)
        proposed_by: Who/what created the proposal
        approved_by: Who approved the proposal
        rejected_by: Who rejected the proposal
        created_at: When the proposal was created
        updated_at: When the proposal was last updated
        executed_at: When the proposal was executed
        metadata: Additional proposal metadata
    """

    id: Optional[int] = Field(
        default=None,
        description="Unique proposal identifier",
    )
    app_uid: str = Field(
        ...,
        description="Application identifier",
        min_length=1,
        max_length=255,
    )
    proposal_type: ProposalType = Field(
        ...,
        description="Type of proposal",
    )
    state: ProposalState = Field(
        default=ProposalState.PENDING,
        description="Current proposal state",
    )
    diff: dict[str, Any] = Field(
        default_factory=dict,
        description="Changes to be made",
    )
    rationale: str = Field(
        ...,
        description="Explanation for this proposal",
        min_length=1,
    )
    risk_score: float = Field(
        default=0.0,
        description="Risk assessment (0-100, lower is safer)",
        ge=0.0,
        le=100.0,
    )
    proposed_by: str = Field(
        default="matrix-ai",
        description="Who/what created the proposal",
        max_length=255,
    )
    approved_by: Optional[str] = Field(
        default=None,
        description="Who approved the proposal",
        max_length=255,
    )
    rejected_by: Optional[str] = Field(
        default=None,
        description="Who rejected the proposal",
        max_length=255,
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When proposal was created",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When proposal was last updated",
    )
    executed_at: Optional[datetime] = Field(
        default=None,
        description="When proposal was executed",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional proposal metadata",
    )

    def is_pending(self) -> bool:
        """
        Check if proposal is pending review.

        Returns:
            True if state is PENDING
        """
        return self.state == ProposalState.PENDING

    def is_approved(self) -> bool:
        """
        Check if proposal is approved.

        Returns:
            True if state is APPROVED
        """
        return self.state == ProposalState.APPROVED

    def is_rejected(self) -> bool:
        """
        Check if proposal is rejected.

        Returns:
            True if state is REJECTED
        """
        return self.state == ProposalState.REJECTED

    def is_completed(self) -> bool:
        """
        Check if proposal execution is completed.

        Returns:
            True if state is COMPLETED
        """
        return self.state == ProposalState.COMPLETED

    def is_low_risk(self) -> bool:
        """
        Check if proposal is low risk.

        Returns:
            True if risk_score is below 30
        """
        return self.risk_score < 30.0

    def is_high_risk(self) -> bool:
        """
        Check if proposal is high risk.

        Returns:
            True if risk_score is above 70
        """
        return self.risk_score > 70.0

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "id": 456,
                "app_uid": "app-123",
                "proposal_type": "lkg_pin",
                "state": "pending",
                "diff": {
                    "action": "pin_version",
                    "from_version": "1.2.4",
                    "to_version": "1.2.3",
                },
                "rationale": "Version 1.2.4 has failing health checks",
                "risk_score": 15.0,
                "proposed_by": "matrix-ai",
                "created_at": "2025-01-15T10:30:00Z",
                "updated_at": "2025-01-15T10:30:00Z",
            }
        }
