"""Unit tests for proposal models."""

from matrix_system.models.proposal import (
    Proposal,
    ProposalState,
    ProposalType,
)


class TestProposalState:
    """Test cases for ProposalState enum."""

    def test_proposal_states(self) -> None:
        """Test that all proposal states are defined."""
        assert ProposalState.PENDING == "pending"
        assert ProposalState.APPROVED == "approved"
        assert ProposalState.REJECTED == "rejected"
        assert ProposalState.EXECUTING == "executing"
        assert ProposalState.COMPLETED == "completed"
        assert ProposalState.FAILED == "failed"


class TestProposalType:
    """Test cases for ProposalType enum."""

    def test_proposal_types(self) -> None:
        """Test that all proposal types are defined."""
        assert ProposalType.LKG_PIN == "lkg_pin"
        assert ProposalType.VERSION_ROLLBACK == "version_rollback"
        assert ProposalType.CACHE_WARMUP == "cache_warmup"


class TestProposal:
    """Test cases for Proposal model."""

    def test_create_proposal(self) -> None:
        """Test creating a valid proposal."""
        proposal = Proposal(
            app_uid="test-app",
            proposal_type=ProposalType.LKG_PIN,
            rationale="Version 1.2.4 has failing health checks",
            risk_score=15.0,
        )
        assert proposal.app_uid == "test-app"
        assert proposal.proposal_type == ProposalType.LKG_PIN
        assert proposal.rationale == "Version 1.2.4 has failing health checks"
        assert proposal.risk_score == 15.0

    def test_proposal_defaults(self) -> None:
        """Test default values for proposals."""
        proposal = Proposal(
            app_uid="test-app",
            proposal_type=ProposalType.LKG_PIN,
            rationale="Test rationale",
        )
        assert proposal.state == ProposalState.PENDING
        assert proposal.risk_score == 0.0
        assert proposal.proposed_by == "matrix-ai"
        assert proposal.diff == {}
        assert proposal.metadata == {}

    def test_is_pending(self) -> None:
        """Test is_pending method."""
        proposal = Proposal(
            app_uid="test-app",
            proposal_type=ProposalType.LKG_PIN,
            rationale="Test",
            state=ProposalState.PENDING,
        )
        assert proposal.is_pending() is True
        assert proposal.is_approved() is False

    def test_is_approved(self) -> None:
        """Test is_approved method."""
        proposal = Proposal(
            app_uid="test-app",
            proposal_type=ProposalType.LKG_PIN,
            rationale="Test",
            state=ProposalState.APPROVED,
        )
        assert proposal.is_approved() is True
        assert proposal.is_pending() is False

    def test_is_low_risk(self) -> None:
        """Test is_low_risk method."""
        proposal = Proposal(
            app_uid="test-app",
            proposal_type=ProposalType.LKG_PIN,
            rationale="Test",
            risk_score=25.0,
        )
        assert proposal.is_low_risk() is True
        assert proposal.is_high_risk() is False

    def test_is_high_risk(self) -> None:
        """Test is_high_risk method."""
        proposal = Proposal(
            app_uid="test-app",
            proposal_type=ProposalType.LKG_PIN,
            rationale="Test",
            risk_score=85.0,
        )
        assert proposal.is_high_risk() is True
        assert proposal.is_low_risk() is False
