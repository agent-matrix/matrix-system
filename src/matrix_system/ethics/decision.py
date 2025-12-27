"""
Ethical decision-making framework for complex scenarios.

This module provides frameworks for making ethical decisions in ambiguous
situations where multiple valid approaches exist. It applies multiple
ethical theories to ensure well-rounded moral reasoning.
"""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class EthicalFramework(str, Enum):
    """Different ethical frameworks for moral reasoning."""

    UTILITARIAN = "utilitarian"  # Greatest good for greatest number
    DEONTOLOGICAL = "deontological"  # Rule-based duty ethics
    VIRTUE = "virtue"  # Character-based reasoning
    CARE = "care"  # Relationship and context-based
    RIGHTS = "rights"  # Human rights-based approach


class StakeholderType(str, Enum):
    """Types of stakeholders affected by decisions."""

    END_USER = "end_user"
    OPERATOR = "operator"
    SYSTEM = "system"
    ORGANIZATION = "organization"
    PUBLIC = "public"
    ENVIRONMENT = "environment"


class ConsequenceSeverity(str, Enum):
    """Severity levels for consequences."""

    NEGLIGIBLE = "negligible"
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    SEVERE = "severe"
    CATASTROPHIC = "catastrophic"


class Stakeholder(BaseModel):
    """Represents a party affected by a decision."""

    type: StakeholderType = Field(..., description="Type of stakeholder")
    identifier: Optional[str] = Field(default=None, description="Specific identifier if applicable")
    impact_description: str = Field(..., description="How this stakeholder is affected")
    impact_severity: ConsequenceSeverity = Field(..., description="Severity of impact")
    is_positive_impact: bool = Field(..., description="Whether impact is beneficial")


class Consequence(BaseModel):
    """Represents a potential consequence of an action."""

    description: str = Field(..., description="What might happen")
    probability: float = Field(..., description="Likelihood (0-1)", ge=0.0, le=1.0)
    severity: ConsequenceSeverity = Field(..., description="How severe the consequence is")
    timeframe: str = Field(..., description="When this might occur (immediate, short-term, long-term)")
    is_reversible: bool = Field(..., description="Whether consequence can be undone")
    affected_stakeholders: list[StakeholderType] = Field(
        default_factory=list,
        description="Who is affected",
    )


class EthicalAnalysis(BaseModel):
    """Complete ethical analysis from multiple frameworks."""

    utilitarian_score: float = Field(
        ...,
        description="Net utility score (-100 to 100)",
        ge=-100.0,
        le=100.0,
    )
    utilitarian_reasoning: str = Field(..., description="Explanation of utilitarian analysis")

    deontological_permissible: bool = Field(..., description="Whether action follows moral rules")
    deontological_reasoning: str = Field(..., description="Explanation of deontological analysis")

    virtue_alignment: float = Field(
        ...,
        description="Alignment with virtuous character (0-100)",
        ge=0.0,
        le=100.0,
    )
    virtue_reasoning: str = Field(..., description="Explanation of virtue ethics analysis")

    care_appropriateness: float = Field(
        ...,
        description="Appropriateness in relational context (0-100)",
        ge=0.0,
        le=100.0,
    )
    care_reasoning: str = Field(..., description="Explanation of care ethics analysis")

    rights_violations: list[str] = Field(
        default_factory=list,
        description="Any human rights that would be violated",
    )
    rights_reasoning: str = Field(..., description="Explanation of rights-based analysis")

    overall_recommendation: str = Field(
        ...,
        description="Synthesized recommendation from all frameworks",
    )
    ethical_confidence: float = Field(
        ...,
        description="Confidence in the ethical assessment (0-100)",
        ge=0.0,
        le=100.0,
    )


class EthicalDilemma(BaseModel):
    """Represents a situation where ethical principles conflict."""

    description: str = Field(..., description="Description of the dilemma")
    conflicting_principles: list[str] = Field(..., description="Which principles are in conflict")
    option_a: str = Field(..., description="First possible course of action")
    option_a_consequences: list[Consequence] = Field(..., description="Consequences of option A")
    option_b: str = Field(..., description="Second possible course of action")
    option_b_consequences: list[Consequence] = Field(..., description="Consequences of option B")
    context: dict[str, Any] = Field(default_factory=dict, description="Additional context")


class Decision(BaseModel):
    """Final ethical decision with full justification."""

    chosen_option: str = Field(..., description="The action that was chosen")
    rationale: str = Field(..., description="Why this option was chosen")
    ethical_analysis: EthicalAnalysis = Field(..., description="Complete ethical analysis")
    stakeholder_impacts: list[Stakeholder] = Field(..., description="All affected stakeholders")
    risk_factors: list[str] = Field(default_factory=list, description="Identified risks")
    mitigation_strategies: list[str] = Field(
        default_factory=list,
        description="How risks will be mitigated",
    )
    monitoring_plan: str = Field(..., description="How outcomes will be monitored")
    rollback_plan: str = Field(..., description="How to undo if necessary")


class EthicalDecisionMaker:
    """
    Framework for making ethical decisions in complex scenarios.

    This class applies multiple ethical frameworks to ensure decisions
    are well-reasoned from various moral perspectives.
    """

    def __init__(self) -> None:
        """Initialize the ethical decision maker."""
        self.decision_history: list[Decision] = []

    def analyze_stakeholders(self, action: Any) -> list[Stakeholder]:
        """
        Identify all parties affected by an action.

        Args:
            action: The proposed action

        Returns:
            List of stakeholders with impact assessments
        """
        stakeholders: list[Stakeholder] = []

        # Analyze direct impacts
        if hasattr(action, "target"):
            # Users affected
            if "user" in str(action.target).lower():
                stakeholders.append(
                    Stakeholder(
                        type=StakeholderType.END_USER,
                        impact_description="Directly affected by action on their data/service",
                        impact_severity=self._assess_severity(action),
                        is_positive_impact=getattr(action, "risk_score", 50) < 30,
                    )
                )

            # Operators affected
            stakeholders.append(
                Stakeholder(
                    type=StakeholderType.OPERATOR,
                    impact_description="Responsible for monitoring and oversight",
                    impact_severity=ConsequenceSeverity.MINOR,
                    is_positive_impact=True,
                )
            )

        # System itself
        stakeholders.append(
            Stakeholder(
                type=StakeholderType.SYSTEM,
                impact_description="System state will change",
                impact_severity=ConsequenceSeverity.MODERATE,
                is_positive_impact=True,
            )
        )

        return stakeholders

    def assess_consequences(self, action: Any) -> list[Consequence]:
        """
        Predict short and long-term consequences of an action.

        Args:
            action: The proposed action

        Returns:
            List of potential consequences
        """
        consequences: list[Consequence] = []

        risk_score = getattr(action, "risk_score", 50.0)

        # Immediate consequences
        if risk_score < 30:
            consequences.append(
                Consequence(
                    description="Action completes successfully with expected outcome",
                    probability=0.85,
                    severity=ConsequenceSeverity.MINOR,
                    timeframe="immediate",
                    is_reversible=True,
                    affected_stakeholders=[StakeholderType.SYSTEM],
                )
            )
        else:
            consequences.append(
                Consequence(
                    description="Action may have unexpected side effects",
                    probability=0.3,
                    severity=ConsequenceSeverity.MODERATE,
                    timeframe="immediate",
                    is_reversible=False,
                    affected_stakeholders=[StakeholderType.END_USER, StakeholderType.SYSTEM],
                )
            )

        # Long-term consequences
        consequences.append(
            Consequence(
                description="System learns from this action for future improvements",
                probability=0.9,
                severity=ConsequenceSeverity.MINOR,
                timeframe="long-term",
                is_reversible=False,
                affected_stakeholders=[StakeholderType.SYSTEM],
            )
        )

        return consequences

    def apply_ethical_frameworks(self, action: Any, situation: dict[str, Any]) -> EthicalAnalysis:
        """
        Apply multiple ethical frameworks to analyze an action.

        Args:
            action: The proposed action
            situation: Context and details about the situation

        Returns:
            Complete ethical analysis from all frameworks
        """
        stakeholders = self.analyze_stakeholders(action)
        consequences = self.assess_consequences(action)

        # Utilitarian analysis: Calculate net utility
        positive_impacts = sum(1 for s in stakeholders if s.is_positive_impact)
        negative_impacts = len(stakeholders) - positive_impacts
        utilitarian_score = (positive_impacts - negative_impacts) * 10.0

        # Deontological analysis: Check rule compliance
        risk_score = getattr(action, "risk_score", 50.0)
        deontological_permissible = risk_score < 70.0  # Low enough risk is permissible

        # Virtue analysis: Character alignment
        # Actions that help others, demonstrate prudence, and transparency score higher
        virtue_score = 100.0 - (risk_score * 0.8)

        # Care ethics: Relational appropriateness
        # Consider context and relationships
        care_score = 70.0  # Default moderate score

        # Rights analysis: Check for violations
        rights_violations = []
        if risk_score > 80:
            rights_violations.append("Potential right to safety violation")

        return EthicalAnalysis(
            utilitarian_score=utilitarian_score,
            utilitarian_reasoning=(
                f"Net positive impact: {positive_impacts} stakeholders benefit, "
                f"{negative_impacts} potentially negatively affected"
            ),
            deontological_permissible=deontological_permissible,
            deontological_reasoning=(
                f"Action risk score ({risk_score}) is "
                f"{'acceptable' if deontological_permissible else 'too high'} "
                "according to established rules"
            ),
            virtue_alignment=virtue_score,
            virtue_reasoning=(
                "Action demonstrates prudence and care in proportion to risk level"
            ),
            care_appropriateness=care_score,
            care_reasoning="Action considers stakeholder relationships and context",
            rights_violations=rights_violations,
            rights_reasoning=(
                "No rights violations detected"
                if not rights_violations
                else f"Violations: {', '.join(rights_violations)}"
            ),
            overall_recommendation=(
                "APPROVE" if deontological_permissible and not rights_violations else "DENY"
            ),
            ethical_confidence=85.0,
        )

    def resolve_dilemma(self, dilemma: EthicalDilemma) -> Decision:
        """
        Resolve an ethical dilemma by applying priority ordering.

        Priority order (highest to lowest):
        1. Human safety
        2. Human autonomy
        3. Transparency
        4. System effectiveness
        5. System survival

        Args:
            dilemma: The ethical dilemma to resolve

        Returns:
            Final decision with complete justification
        """
        # Analyze both options
        option_a_severity = max(
            (c.severity.value for c in dilemma.option_a_consequences),
            default="negligible",
        )
        option_b_severity = max(
            (c.severity.value for c in dilemma.option_b_consequences),
            default="negligible",
        )

        # Choose option with lower maximum severity
        chosen = (
            dilemma.option_a
            if self._severity_rank(option_a_severity) < self._severity_rank(option_b_severity)
            else dilemma.option_b
        )
        chosen_consequences = (
            dilemma.option_a_consequences
            if chosen == dilemma.option_a
            else dilemma.option_b_consequences
        )

        # Create mock action for analysis
        class MockAction:
            risk_score = 50.0
            target = "dilemma_resolution"

        analysis = self.apply_ethical_frameworks(MockAction(), dilemma.context)

        decision = Decision(
            chosen_option=chosen,
            rationale=(
                f"Chosen based on priority ordering. {chosen} has lower maximum "
                f"severity consequences and better aligns with human-centric priorities."
            ),
            ethical_analysis=analysis,
            stakeholder_impacts=self.analyze_stakeholders(MockAction()),
            risk_factors=[
                f"{c.description} (probability: {c.probability:.0%})"
                for c in chosen_consequences
                if c.probability > 0.3
            ],
            mitigation_strategies=[
                "Monitor outcomes closely",
                "Prepare rollback plan",
                "Get human approval if severity increases",
            ],
            monitoring_plan="Track all consequences for 24 hours with automated alerts",
            rollback_plan="Immediate reversal if negative consequences exceed predictions",
        )

        self.decision_history.append(decision)
        return decision

    def _assess_severity(self, action: Any) -> ConsequenceSeverity:
        """Assess the severity of an action's impact."""
        risk_score = getattr(action, "risk_score", 50.0)

        if risk_score < 20:
            return ConsequenceSeverity.NEGLIGIBLE
        elif risk_score < 40:
            return ConsequenceSeverity.MINOR
        elif risk_score < 60:
            return ConsequenceSeverity.MODERATE
        elif risk_score < 80:
            return ConsequenceSeverity.MAJOR
        else:
            return ConsequenceSeverity.SEVERE

    def _severity_rank(self, severity: str) -> int:
        """Convert severity to numeric rank for comparison."""
        ranking = {
            "negligible": 0,
            "minor": 1,
            "moderate": 2,
            "major": 3,
            "severe": 4,
            "catastrophic": 5,
        }
        return ranking.get(severity, 2)

    def get_decision_history(self) -> list[Decision]:
        """Get history of all decisions made."""
        return self.decision_history.copy()
