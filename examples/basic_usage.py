#!/usr/bin/env python3
"""
Basic usage example for Matrix System SDK.

This example demonstrates how to use the Matrix System SDK to:
- Initialize the client
- Check service health
- Create health check models
- Work with events and proposals

Author: Ruslan Magana
Website: https://ruslanmv.com
"""

from matrix_system import __version__
from matrix_system.api.client import MatrixClient
from matrix_system.api.exceptions import MatrixAPIError, MatrixAuthError, MatrixTimeoutError
from matrix_system.models.events import Event, EventType
from matrix_system.models.health import HealthCheck, HealthStatus, HealthSummary
from matrix_system.models.proposal import Proposal, ProposalState, ProposalType
from matrix_system.utils.config import get_config
from matrix_system.utils.logger import get_logger, setup_logging


def main() -> None:
    """Run the basic usage examples."""
    # Setup logging
    setup_logging(log_level="INFO")
    logger = get_logger(__name__)

    logger.info("matrix_system_example_started", version=__version__)

    # Get configuration
    config = get_config()
    logger.info(
        "configuration_loaded",
        hub_url=str(config.matrix_hub_url),
        timeout=config.timeout,
    )

    # Example 1: Health Check with API Client
    print("\n=== Example 1: API Health Check ===")
    try:
        with MatrixClient(config=config) as client:
            health_data = client.health_check("hub")
            print(f"✓ Matrix Hub is {health_data.get('status', 'unknown')}")
            logger.info("health_check_success", service="hub", data=health_data)
    except MatrixAuthError as e:
        print(f"✗ Authentication failed: {e}")
        logger.error("auth_error", error=str(e))
    except MatrixTimeoutError as e:
        print(f"✗ Request timed out: {e}")
        logger.error("timeout_error", error=str(e))
    except MatrixAPIError as e:
        print(f"✗ API error: {e}")
        logger.error("api_error", error=str(e))

    # Example 2: Creating Health Check Models
    print("\n=== Example 2: Health Check Models ===")
    health_check = HealthCheck(
        app_uid="example-app-001",
        check_type="http",
        result="pass",
        status=HealthStatus.HEALTHY,
        score=95.5,
        latency_ms=45.2,
        reasons={"message": "All systems operational"},
    )

    print(f"App UID: {health_check.app_uid}")
    print(f"Status: {health_check.status.value}")
    print(f"Score: {health_check.score}")
    print(f"Is Healthy: {health_check.is_healthy()}")
    print(f"Latency: {health_check.latency_ms}ms")

    # Example 3: Health Summary
    print("\n=== Example 3: Health Summary ===")
    summary = HealthSummary(
        total_entities=100,
        healthy_count=92,
        degraded_count=5,
        unhealthy_count=3,
        unknown_count=0,
        average_score=91.2,
    )

    print(f"Total Entities: {summary.total_entities}")
    print(f"Healthy: {summary.healthy_count} ({summary.health_percentage()}%)")
    print(f"Degraded: {summary.degraded_count}")
    print(f"Unhealthy: {summary.unhealthy_count}")
    print(f"Average Score: {summary.average_score}")

    # Example 4: Creating Events
    print("\n=== Example 4: Event Tracking ===")
    event = Event(
        event_type=EventType.PLAN_CREATED,
        app_uid="example-app-001",
        payload={
            "action": "pin_lkg",
            "version": "1.2.3",
            "reason": "Current version unstable",
        },
        actor="matrix-guardian",
        metadata={
            "severity": "medium",
            "automated": True,
        },
    )

    print(f"Event Type: {event.event_type.value}")
    print(f"App UID: {event.app_uid}")
    print(f"Actor: {event.actor}")
    print(f"Is Critical: {event.is_critical()}")
    print(f"Is Success: {event.is_success()}")
    print(f"Payload: {event.payload}")

    # Example 5: Creating Proposals
    print("\n=== Example 5: Proposals ===")
    proposal = Proposal(
        app_uid="example-app-001",
        proposal_type=ProposalType.LKG_PIN,
        state=ProposalState.PENDING,
        rationale="Version 1.2.4 has failing health checks. Pinning to last known good version 1.2.3.",
        risk_score=15.0,
        diff={
            "action": "pin_version",
            "from_version": "1.2.4",
            "to_version": "1.2.3",
            "estimated_impact": "low",
        },
        proposed_by="matrix-ai",
        metadata={
            "health_score_before": 65.0,
            "expected_health_score": 95.0,
        },
    )

    print(f"Proposal ID: {proposal.id or 'Not assigned'}")
    print(f"Type: {proposal.proposal_type.value}")
    print(f"State: {proposal.state.value}")
    print(f"Risk Score: {proposal.risk_score}")
    print(f"Is Low Risk: {proposal.is_low_risk()}")
    print(f"Is High Risk: {proposal.is_high_risk()}")
    print(f"Rationale: {proposal.rationale}")
    print(f"Diff: {proposal.diff}")

    # Example 6: Checking Different Health States
    print("\n=== Example 6: Health State Checks ===")

    states = [
        ("healthy", HealthStatus.HEALTHY, 98.0),
        ("degraded", HealthStatus.DEGRADED, 65.0),
        ("unhealthy", HealthStatus.UNHEALTHY, 25.0),
    ]

    for name, status, score in states:
        check = HealthCheck(
            app_uid=f"app-{name}",
            check_type="http",
            result="pass" if status == HealthStatus.HEALTHY else "fail",
            status=status,
            score=score,
        )
        print(f"\n{name.upper()}:")
        print(f"  Status: {check.status.value}")
        print(f"  Score: {check.score}")
        print(f"  Is Healthy: {check.is_healthy()}")
        print(f"  Is Degraded: {check.is_degraded()}")
        print(f"  Is Unhealthy: {check.is_unhealthy()}")

    logger.info("matrix_system_example_completed")
    print("\n=== All Examples Completed Successfully! ===\n")


if __name__ == "__main__":
    main()
