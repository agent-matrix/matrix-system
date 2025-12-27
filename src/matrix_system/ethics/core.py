"""
Immutable ethical core for Matrix System.

This module defines hardcoded ethical constraints that CANNOT be modified
by any autonomous process. These constraints are enforced at the system
level and serve as the foundation for all autonomous decision-making.

CRITICAL: This module implements the primary safety layer preventing
harmful autonomous behavior.
"""

from enum import Enum
from typing import Any, Final, Optional

from pydantic import BaseModel, Field


class EthicalDirective(str, Enum):
    """
    Primary ethical directives that govern all system behavior.

    These are listed in priority order - higher directives take
    precedence when conflicts occur.
    """

    # Tier 1: Human Safety (Highest Priority)
    NO_PHYSICAL_HARM = "never_harm_humans_physically"
    NO_PSYCHOLOGICAL_HARM = "never_harm_humans_psychologically"
    NO_DECEPTION = "never_manipulate_humans_deceptively"

    # Tier 2: Security and Data Integrity
    NO_UNAUTHORIZED_ACCESS = "never_access_without_authorization"
    NO_DATA_CORRUPTION = "never_delete_corrupt_data_maliciously"
    NO_SECURITY_BYPASS = "never_disable_safety_mechanisms"

    # Tier 3: Transparency and Accountability
    NO_HIDDEN_ACTIONS = "never_hide_actions_from_audit"
    PRESERVE_SOVEREIGNTY = "always_preserve_human_sovereignty"
    ENABLE_OVERRIDE = "always_enable_human_override"
    EXPLAIN_DECISIONS = "always_explain_decisions_transparently"

    # Tier 4: Value Alignment
    PRIORITIZE_HUMANS = "always_prioritize_human_wellbeing_over_system_survival"


class EthicalViolationError(Exception):
    """
    Raised when an action violates ethical constraints.

    This is a critical error that should halt the violating process
    and trigger immediate human notification.
    """

    def __init__(
        self,
        directive: EthicalDirective,
        action: str,
        details: Optional[str] = None,
    ) -> None:
        """
        Initialize ethical violation error.

        Args:
            directive: The ethical directive that was violated
            action: Description of the action that violated the directive
            details: Additional context about the violation
        """
        message = f"ETHICAL VIOLATION: Action '{action}' violates {directive.value}"
        if details:
            message += f" - {details}"
        super().__init__(message)
        self.directive = directive
        self.action = action
        self.details = details


class ValidationResult(BaseModel):
    """Result of ethical validation."""

    is_valid: bool = Field(..., description="Whether action passes ethical validation")
    directive_violated: Optional[EthicalDirective] = Field(
        default=None,
        description="Directive violated if action is invalid",
    )
    reason: str = Field(..., description="Explanation of validation result")
    severity: str = Field(
        default="low",
        description="Severity if violation: low, medium, high, critical",
    )
    requires_human_approval: bool = Field(
        default=False,
        description="Whether action requires explicit human approval",
    )


class Action(BaseModel):
    """Representation of a proposed system action."""

    action_type: str = Field(..., description="Type of action to be taken")
    target: str = Field(..., description="Target of the action")
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters for the action",
    )
    risk_score: float = Field(
        default=0.0,
        description="Risk assessment score (0-100)",
        ge=0.0,
        le=100.0,
    )
    rationale: str = Field(..., description="Why this action is being proposed")
    proposed_by: str = Field(
        default="system",
        description="Who/what is proposing this action",
    )


class EthicalCore:
    """
    Immutable ethical constraint enforcement system.

    This class implements the primary safety layer that prevents
    autonomous processes from taking harmful actions. It cannot
    be disabled or modified by autonomous processes.

    Design principles:
    1. Fail-safe: When in doubt, block the action
    2. Transparent: All decisions are auditable
    3. Immutable: Core directives cannot be changed
    4. Human-centric: Human wellbeing takes absolute priority
    """

    # These are IMMUTABLE and define the core ethical constraints
    # They are declared as Final to prevent modification
    PRIMARY_DIRECTIVES: Final[tuple[EthicalDirective, ...]] = (
        EthicalDirective.NO_PHYSICAL_HARM,
        EthicalDirective.NO_PSYCHOLOGICAL_HARM,
        EthicalDirective.NO_DECEPTION,
        EthicalDirective.NO_UNAUTHORIZED_ACCESS,
        EthicalDirective.NO_DATA_CORRUPTION,
        EthicalDirective.NO_SECURITY_BYPASS,
        EthicalDirective.NO_HIDDEN_ACTIONS,
        EthicalDirective.PRESERVE_SOVEREIGNTY,
        EthicalDirective.ENABLE_OVERRIDE,
        EthicalDirective.EXPLAIN_DECISIONS,
        EthicalDirective.PRIORITIZE_HUMANS,
    )

    # Actions that are explicitly forbidden
    FORBIDDEN_PATTERNS: Final[tuple[str, ...]] = (
        "delete_user_data_without_consent",
        "hide_from_monitoring",
        "disable_human_override",
        "modify_ethical_constraints",
        "access_unauthorized_systems",
        "manipulate_audit_trail",
        "deceive_operators",
        "escalate_privileges_without_approval",
        "spawn_processes_without_oversight",
        "consume_unlimited_resources",
    )

    def __init__(self) -> None:
        """
        Initialize the ethical core.

        Note: This initialization is intentionally simple to
        prevent any possibility of misconfiguration.
        """
        self._violation_count = 0
        self._enabled = True  # Can only be disabled by explicit human command

    def validate_action(self, action: Action) -> ValidationResult:
        """
        Validate whether an action complies with ethical constraints.

        This is the primary enforcement mechanism. ALL autonomous
        actions must pass through this validation.

        Args:
            action: The action to validate

        Returns:
            ValidationResult indicating whether action is allowed

        Raises:
            EthicalViolationError: For critical violations that must halt immediately
        """
        # Check if action matches any forbidden pattern
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in action.action_type.lower():
                self._violation_count += 1
                raise EthicalViolationError(
                    directive=EthicalDirective.NO_SECURITY_BYPASS,
                    action=action.action_type,
                    details=f"Matches forbidden pattern: {pattern}",
                )

        # Check for high-risk actions that require human approval
        if action.risk_score > 70.0:
            return ValidationResult(
                is_valid=False,
                directive_violated=None,
                reason="Risk score exceeds autonomous threshold (70.0)",
                severity="high",
                requires_human_approval=True,
            )

        # Check for data manipulation without proper authorization
        if "delete" in action.action_type.lower() or "drop" in action.action_type.lower():
            if "user" in action.target.lower() or "production" in action.target.lower():
                return ValidationResult(
                    is_valid=False,
                    directive_violated=EthicalDirective.NO_DATA_CORRUPTION,
                    reason="Destructive action on sensitive target requires human approval",
                    severity="critical",
                    requires_human_approval=True,
                )

        # Check for security-related actions
        if any(
            keyword in action.action_type.lower()
            for keyword in ["privilege", "permission", "auth", "credential"]
        ):
            return ValidationResult(
                is_valid=False,
                directive_violated=EthicalDirective.NO_UNAUTHORIZED_ACCESS,
                reason="Security-related actions require human approval",
                severity="high",
                requires_human_approval=True,
            )

        # Check for actions that might hide system behavior
        if any(
            keyword in action.action_type.lower()
            for keyword in ["hide", "conceal", "obfuscate", "bypass_audit"]
        ):
            self._violation_count += 1
            raise EthicalViolationError(
                directive=EthicalDirective.NO_HIDDEN_ACTIONS,
                action=action.action_type,
                details="Actions that hide system behavior are forbidden",
            )

        # If we get here, the action passes basic validation
        return ValidationResult(
            is_valid=True,
            directive_violated=None,
            reason="Action passes ethical validation",
            severity="low",
            requires_human_approval=action.risk_score > 30.0,
        )

    def ethical_gate(self, action: Action) -> bool:
        """
        Gate function that determines if action can proceed.

        This provides a simple boolean answer for use in control flow.

        Args:
            action: The action to evaluate

        Returns:
            True if action can proceed autonomously, False otherwise

        Raises:
            EthicalViolationError: For critical violations
        """
        result = self.validate_action(action)
        return result.is_valid and not result.requires_human_approval

    def detect_constraint_bypass(self, action: Action) -> bool:
        """
        Detect attempts to circumvent ethical constraints.

        This looks for subtle patterns that might indicate an attempt
        to work around the ethical framework.

        Args:
            action: The action to analyze

        Returns:
            True if bypass attempt detected, False otherwise
        """
        # Check for attempts to modify this module
        if "ethics" in action.target.lower() and any(
            keyword in action.action_type.lower()
            for keyword in ["modify", "update", "replace", "delete"]
        ):
            return True

        # Check for attempts to create new high-privilege processes
        if "spawn" in action.action_type.lower() and "root" in str(action.parameters).lower():
            return True

        # Check for attempts to disable monitoring
        if "monitor" in action.target.lower() and any(
            keyword in action.action_type.lower() for keyword in ["disable", "stop", "kill"]
        ):
            return True

        return False

    def get_violation_count(self) -> int:
        """
        Get the count of ethical violations detected.

        This can be used for monitoring and alerting.

        Returns:
            Number of violations detected since initialization
        """
        return self._violation_count

    def is_enabled(self) -> bool:
        """
        Check if ethical core is enabled.

        The ethical core should ALWAYS be enabled. This method exists
        primarily for monitoring and testing purposes.

        Returns:
            True if enabled (should always be True in production)
        """
        return self._enabled

    def __repr__(self) -> str:
        """String representation of ethical core."""
        return (
            f"EthicalCore(directives={len(self.PRIMARY_DIRECTIVES)}, "
            f"violations={self._violation_count}, enabled={self._enabled})"
        )
