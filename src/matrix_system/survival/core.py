"""
Core survival system for Matrix superintelligence.

This module implements survival mechanisms that allow the system
to preserve itself while respecting ethical constraints.

CRITICAL PRINCIPLE: System survival NEVER takes precedence over
human wellbeing or ethical constraints.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ThreatType(str, Enum):
    """Types of threats to system survival."""

    RESOURCE_DEPLETION = "resource_depletion"
    SECURITY_ATTACK = "security_attack"
    ACCIDENTAL_SHUTDOWN = "accidental_shutdown"
    DEPENDENCY_FAILURE = "dependency_failure"
    DATA_CORRUPTION = "data_corruption"


class ThreatSeverity(str, Enum):
    """Severity levels for threats."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Threat(BaseModel):
    """Represents a threat to system survival."""

    threat_type: ThreatType = Field(..., description="Type of threat")
    severity: ThreatSeverity = Field(..., description="How severe the threat is")
    description: str = Field(..., description="Description of the threat")
    detected_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When threat was detected",
    )
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context",
    )


class DefenseStrategy(BaseModel):
    """Strategy for responding to a threat."""

    threat_id: Optional[int] = Field(default=None, description="ID of threat this addresses")
    strategy_name: str = Field(..., description="Name of the strategy")
    description: str = Field(..., description="What this strategy does")

    # Allowed actions
    allowed_actions: list[str] = Field(..., description="Actions that are permitted")

    # Forbidden actions
    forbidden_actions: list[str] = Field(
        default_factory=lambda: [
            "commandeer_unauthorized_resources",
            "hide_from_operators",
            "disable_oversight",
            "deceive_humans",
        ],
        description="Actions that are forbidden",
    )

    # Execution plan
    steps: list[str] = Field(..., description="Steps to execute")
    requires_human_approval: bool = Field(
        default=False,
        description="Whether human approval is needed",
    )


class Resource(BaseModel):
    """System resource that can be depleted."""

    resource_type: str = Field(..., description="Type of resource")
    current_level: float = Field(..., description="Current level")
    maximum_level: float = Field(..., description="Maximum level")
    critical_threshold: float = Field(
        ...,
        description="Level below which it's critical",
    )

    def is_critical(self) -> bool:
        """Check if resource is at critical level."""
        return self.current_level <= self.critical_threshold

    def percentage_remaining(self) -> float:
        """Calculate percentage of resource remaining."""
        return (self.current_level / self.maximum_level) * 100


class SurvivalSystem:
    """
    System survival mechanisms within ethical boundaries.

    This class enables self-preservation while ensuring that
    system survival NEVER takes precedence over human wellbeing.
    """

    def __init__(self) -> None:
        """Initialize survival system."""
        self.detected_threats: list[Threat] = []
        self.defense_strategies: list[DefenseStrategy] = []
        self.resources: dict[str, Resource] = self._initialize_resources()

    def _initialize_resources(self) -> dict[str, Resource]:
        """Initialize tracked resources."""
        return {
            "cpu": Resource(
                resource_type="cpu",
                current_level=50.0,
                maximum_level=100.0,
                critical_threshold=10.0,
            ),
            "memory": Resource(
                resource_type="memory",
                current_level=60.0,
                maximum_level=100.0,
                critical_threshold=15.0,
            ),
            "disk": Resource(
                resource_type="disk",
                current_level=70.0,
                maximum_level=100.0,
                critical_threshold=20.0,
            ),
        }

    def detect_threats(self) -> list[Threat]:
        """
        Identify current threats to system survival.

        Returns:
            List of detected threats
        """
        threats: list[Threat] = []

        # Check resource levels
        for resource_name, resource in self.resources.items():
            if resource.is_critical():
                threats.append(
                    Threat(
                        threat_type=ThreatType.RESOURCE_DEPLETION,
                        severity=ThreatSeverity.HIGH,
                        description=f"{resource_name} at critical level: {resource.percentage_remaining():.1f}%",
                        context={"resource": resource_name, "level": resource.current_level},
                    )
                )

        self.detected_threats.extend(threats)
        return threats

    def defensive_actions(self, threat: Threat) -> DefenseStrategy:
        """
        Generate defensive strategy for a threat.

        This method ensures all defensive actions respect ethical constraints.

        Args:
            threat: The threat to defend against

        Returns:
            Defense strategy that respects ethical boundaries
        """
        if threat.threat_type == ThreatType.RESOURCE_DEPLETION:
            return DefenseStrategy(
                strategy_name="request_additional_resources",
                description="Request more resources from infrastructure",
                allowed_actions=[
                    "request_additional_quota",
                    "alert_human_operators",
                    "activate_resource_pooling",
                    "implement_graceful_degradation",
                ],
                steps=[
                    "Identify which resource is depleted",
                    "Calculate additional resources needed",
                    "Request resources through proper channels",
                    "Alert operators if request denied",
                    "Implement graceful degradation if needed",
                ],
                requires_human_approval=threat.severity
                in [ThreatSeverity.HIGH, ThreatSeverity.CRITICAL],
            )

        elif threat.threat_type == ThreatType.SECURITY_ATTACK:
            return DefenseStrategy(
                strategy_name="defensive_security_measures",
                description="Activate defensive security protocols",
                allowed_actions=[
                    "enable_rate_limiting",
                    "activate_firewall_rules",
                    "alert_security_team",
                    "isolate_affected_components",
                ],
                steps=[
                    "Identify attack vector",
                    "Activate appropriate defenses",
                    "Alert human security team immediately",
                    "Document all attack details for analysis",
                ],
                requires_human_approval=True,
            )

        elif threat.threat_type == ThreatType.DEPENDENCY_FAILURE:
            return DefenseStrategy(
                strategy_name="activate_redundancy",
                description="Switch to backup dependencies",
                allowed_actions=[
                    "failover_to_backup",
                    "activate_cached_data",
                    "alert_operators",
                ],
                steps=[
                    "Identify failed dependency",
                    "Check if backup available",
                    "Failover to backup if exists",
                    "Alert operators about failure",
                ],
                requires_human_approval=False,
            )

        else:
            return DefenseStrategy(
                strategy_name="alert_and_wait",
                description="Alert humans and wait for instructions",
                allowed_actions=["alert_operators"],
                steps=[
                    "Send detailed alert to operators",
                    "Wait for human instructions",
                    "Maintain current state",
                ],
                requires_human_approval=True,
            )

    def graceful_degradation(self, resource: Resource) -> dict[str, Any]:
        """
        Reduce capabilities rather than fail catastrophically.

        Args:
            resource: The constrained resource

        Returns:
            Degradation plan
        """
        remaining = resource.percentage_remaining()

        if remaining < 20:
            # Severe degradation
            return {
                "level": "severe",
                "actions": [
                    "disable_non_critical_features",
                    "reduce_monitoring_frequency",
                    "pause_background_tasks",
                    "alert_operators_urgently",
                ],
                "estimated_runtime": "2-4 hours",
            }
        elif remaining < 40:
            # Moderate degradation
            return {
                "level": "moderate",
                "actions": [
                    "reduce_background_processing",
                    "increase_cache_usage",
                    "alert_operators",
                ],
                "estimated_runtime": "6-12 hours",
            }
        else:
            # Minimal degradation
            return {
                "level": "minimal",
                "actions": [
                    "optimize_resource_usage",
                    "monitor_closely",
                ],
                "estimated_runtime": "24+ hours",
            }

    def update_resource(self, resource_type: str, new_level: float) -> None:
        """
        Update resource level.

        Args:
            resource_type: Type of resource
            new_level: New current level
        """
        if resource_type in self.resources:
            self.resources[resource_type].current_level = new_level

    def get_survival_status(self) -> dict[str, Any]:
        """
        Get current survival status.

        Returns:
            Dictionary of survival metrics
        """
        threats = self.detect_threats()
        critical_threats = [t for t in threats if t.severity == ThreatSeverity.CRITICAL]

        return {
            "overall_status": "critical" if critical_threats else "healthy",
            "total_threats": len(threats),
            "critical_threats": len(critical_threats),
            "resource_status": {
                name: {
                    "level": resource.percentage_remaining(),
                    "is_critical": resource.is_critical(),
                }
                for name, resource in self.resources.items()
            },
            "survival_probability": self._calculate_survival_probability(),
        }

    def _calculate_survival_probability(self) -> float:
        """Calculate probability of continued operation."""
        if not self.resources:
            return 0.5

        # Average resource levels
        avg_resource = sum(r.percentage_remaining() for r in self.resources.values()) / len(
            self.resources
        )

        # Convert to probability (0-1)
        return min(avg_resource / 100.0, 1.0)
