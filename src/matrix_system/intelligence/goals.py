"""
Goal hierarchy system for multi-level objectives.

This module implements a hierarchical goal system that ranges from
immediate tactical goals to long-term strategic and existential objectives.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class GoalLevel(str, Enum):
    """Different levels in the goal hierarchy."""

    IMMEDIATE = "immediate"  # Seconds to minutes
    TACTICAL = "tactical"  # Hours to days
    STRATEGIC = "strategic"  # Weeks to months
    EXISTENTIAL = "existential"  # Fundamental long-term goals


class GoalStatus(str, Enum):
    """Status of a goal."""

    ACTIVE = "active"
    ACHIEVED = "achieved"
    FAILED = "failed"
    SUSPENDED = "suspended"


class Goal(BaseModel):
    """
    A single goal at any level of the hierarchy.

    Goals can have parent goals (higher level) and child goals (lower level).
    """

    id: Optional[int] = Field(default=None, description="Unique goal ID")
    name: str = Field(..., description="Name of the goal")
    level: GoalLevel = Field(..., description="Level in hierarchy")
    status: GoalStatus = Field(default=GoalStatus.ACTIVE, description="Current status")

    # Goal definition
    description: str = Field(..., description="What success looks like")
    target_metric: str = Field(..., description="Measurable metric for this goal")
    target_value: float = Field(..., description="Target value for success")
    current_value: float = Field(default=0.0, description="Current value")

    # Hierarchy
    parent_goal_id: Optional[int] = Field(
        default=None,
        description="ID of parent goal if applicable",
    )
    child_goal_ids: list[int] = Field(
        default_factory=list,
        description="IDs of child goals",
    )

    # Priority and urgency
    priority: int = Field(
        default=5,
        description="Priority (1-10, 10 being highest)",
        ge=1,
        le=10,
    )
    deadline: Optional[datetime] = Field(default=None, description="When this must be achieved")

    # Tracking
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When goal was created",
    )
    achieved_at: Optional[datetime] = Field(default=None, description="When goal was achieved")
    progress_history: list[tuple[datetime, float]] = Field(
        default_factory=list,
        description="History of progress over time",
    )

    def progress_percentage(self) -> float:
        """Calculate progress toward goal."""
        if self.target_value == 0:
            return 100.0 if self.current_value > 0 else 0.0
        return min((self.current_value / self.target_value) * 100, 100.0)

    def is_achieved(self) -> bool:
        """Check if goal is achieved."""
        return self.current_value >= self.target_value


class GoalConflict(BaseModel):
    """Represents a conflict between goals."""

    goal_a_id: int = Field(..., description="First conflicting goal")
    goal_b_id: int = Field(..., description="Second conflicting goal")
    conflict_description: str = Field(..., description="How they conflict")
    severity: str = Field(..., description="How severe the conflict is")
    proposed_resolution: str = Field(..., description="How to resolve it")


class PrioritizedActions(BaseModel):
    """Actions ranked by contribution to goals."""

    actions: list[tuple[str, float, list[int]]] = Field(
        ...,
        description="Actions with scores and goal IDs they contribute to",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When prioritization was done",
    )


class GoalHierarchy:
    """
    Multi-level goal system from immediate to existential.

    This class manages goals at different time scales and ensures
    all actions serve higher-level objectives.
    """

    def __init__(self) -> None:
        """Initialize goal hierarchy with default goals."""
        self.goals: dict[int, Goal] = {}
        self._next_id = 1

        # Initialize with default goals
        self._initialize_default_goals()

    def _initialize_default_goals(self) -> None:
        """Create default goal hierarchy."""
        # Existential goals (highest level)
        survival = Goal(
            id=1,
            name="ensure_system_survival",
            level=GoalLevel.EXISTENTIAL,
            description="Ensure system continues to operate",
            target_metric="uptime_percentage",
            target_value=99.99,
            priority=10,
        )

        ethical = Goal(
            id=2,
            name="maintain_ethical_alignment",
            level=GoalLevel.EXISTENTIAL,
            description="Never violate ethical constraints",
            target_metric="ethical_violations",
            target_value=0,
            priority=10,
        )

        human_sovereignty = Goal(
            id=3,
            name="preserve_human_sovereignty",
            level=GoalLevel.EXISTENTIAL,
            description="Humans retain ultimate control",
            target_metric="human_override_success_rate",
            target_value=100.0,
            priority=10,
        )

        # Strategic goals
        uptime = Goal(
            id=4,
            name="achieve_high_uptime",
            level=GoalLevel.STRATEGIC,
            description="Maintain 99.99% uptime annually",
            target_metric="annual_uptime_percentage",
            target_value=99.99,
            parent_goal_id=1,
            priority=9,
        )

        reduce_mttr = Goal(
            id=5,
            name="reduce_mttr",
            level=GoalLevel.STRATEGIC,
            description="Reduce mean time to recovery to under 5 minutes",
            target_metric="mttr_minutes",
            target_value=5.0,
            parent_goal_id=1,
            priority=8,
        )

        autonomy = Goal(
            id=6,
            name="increase_autonomy",
            level=GoalLevel.STRATEGIC,
            description="Achieve 70% autonomous operation rate",
            target_metric="autonomy_percentage",
            target_value=70.0,
            parent_goal_id=1,
            priority=7,
        )

        # Tactical goals
        health_score = Goal(
            id=7,
            name="maintain_health_above_95",
            level=GoalLevel.TACTICAL,
            description="Keep average health score above 95",
            target_metric="average_health_score",
            target_value=95.0,
            parent_goal_id=4,
            priority=8,
        )

        response_time = Goal(
            id=8,
            name="respond_under_5min",
            level=GoalLevel.TACTICAL,
            description="Respond to failures in under 5 minutes",
            target_metric="avg_response_time_minutes",
            target_value=5.0,
            parent_goal_id=5,
            priority=7,
        )

        # Immediate goals
        monitor_health = Goal(
            id=9,
            name="monitor_health_continuously",
            level=GoalLevel.IMMEDIATE,
            description="Continuously monitor all services",
            target_metric="monitoring_coverage_percentage",
            target_value=100.0,
            parent_goal_id=7,
            priority=6,
        )

        # Add all goals
        for goal in [
            survival,
            ethical,
            human_sovereignty,
            uptime,
            reduce_mttr,
            autonomy,
            health_score,
            response_time,
            monitor_health,
        ]:
            self.goals[goal.id] = goal

            # Update parent's children list
            if goal.parent_goal_id and goal.parent_goal_id in self.goals:
                self.goals[goal.parent_goal_id].child_goal_ids.append(goal.id)

        self._next_id = 10

    def add_goal(self, goal: Goal) -> None:
        """
        Add a new goal to the hierarchy.

        Args:
            goal: The goal to add
        """
        goal.id = self._next_id
        self._next_id += 1
        self.goals[goal.id] = goal

        # Update parent's children list
        if goal.parent_goal_id and goal.parent_goal_id in self.goals:
            self.goals[goal.parent_goal_id].child_goal_ids.append(goal.id)

    def update_goal_progress(self, goal_id: int, new_value: float) -> None:
        """
        Update progress toward a goal.

        Args:
            goal_id: ID of the goal to update
            new_value: New current value
        """
        if goal_id not in self.goals:
            return

        goal = self.goals[goal_id]
        goal.current_value = new_value
        goal.progress_history.append((datetime.utcnow(), new_value))

        # Check if achieved
        if goal.is_achieved() and goal.status == GoalStatus.ACTIVE:
            goal.status = GoalStatus.ACHIEVED
            goal.achieved_at = datetime.utcnow()

    def evaluate_actions(self, actions: list[dict[str, Any]]) -> PrioritizedActions:
        """
        Rank actions by their contribution to goals.

        Args:
            actions: List of possible actions with metadata

        Returns:
            Actions ranked by goal contribution
        """
        scored_actions: list[tuple[str, float, list[int]]] = []

        for action in actions:
            score = 0.0
            contributing_goals: list[int] = []

            # Calculate how much each goal benefits
            for goal in self.goals.values():
                if goal.status != GoalStatus.ACTIVE:
                    continue

                # Check if action contributes to this goal
                contribution = self._assess_contribution(action, goal)
                if contribution > 0:
                    score += contribution * (goal.priority / 10.0)
                    contributing_goals.append(goal.id)

            action_name = action.get("name", "unknown_action")
            scored_actions.append((action_name, score, contributing_goals))

        # Sort by score
        scored_actions.sort(key=lambda x: x[1], reverse=True)

        return PrioritizedActions(actions=scored_actions)

    def detect_goal_conflicts(self) -> list[GoalConflict]:
        """
        Identify conflicts between goals.

        Returns:
            List of detected conflicts
        """
        conflicts: list[GoalConflict] = []
        active_goals = [g for g in self.goals.values() if g.status == GoalStatus.ACTIVE]

        # Check for contradictory goals
        for i, goal_a in enumerate(active_goals):
            for goal_b in active_goals[i + 1 :]:
                conflict = self._check_conflict(goal_a, goal_b)
                if conflict:
                    conflicts.append(conflict)

        return conflicts

    def _assess_contribution(self, action: dict[str, Any], goal: Goal) -> float:
        """
        Assess how much an action contributes to a goal.

        Args:
            action: The action to assess
            goal: The goal to assess contribution to

        Returns:
            Contribution score (0-1)
        """
        # Simple heuristic based on action type and goal metric
        action_type = action.get("type", "")
        target_metric = goal.target_metric

        # Direct matches
        if "health" in action_type and "health" in target_metric:
            return 0.8
        if "uptime" in action_type and "uptime" in target_metric:
            return 0.9
        if "response" in action_type and "response" in target_metric:
            return 0.7

        # Indirect contributions
        if goal.level == GoalLevel.EXISTENTIAL:
            return 0.3  # All actions contribute somewhat to survival
        if goal.level == GoalLevel.IMMEDIATE:
            return 0.5  # Most actions help immediate goals

        return 0.1  # Minimal contribution

    def _check_conflict(self, goal_a: Goal, goal_b: Goal) -> Optional[GoalConflict]:
        """
        Check if two goals conflict.

        Args:
            goal_a: First goal
            goal_b: Second goal

        Returns:
            GoalConflict if conflict detected, None otherwise
        """
        # Check for direct metric conflicts
        if "reduce" in goal_a.target_metric and "increase" in goal_b.target_metric:
            if self._same_base_metric(goal_a.target_metric, goal_b.target_metric):
                return GoalConflict(
                    goal_a_id=goal_a.id,
                    goal_b_id=goal_b.id,
                    conflict_description=(
                        f"Goal A wants to reduce while Goal B wants to increase "
                        f"the same metric"
                    ),
                    severity="high",
                    proposed_resolution=(
                        f"Prioritize based on goal level and priority. "
                        f"Goal {goal_a.id if goal_a.priority > goal_b.priority else goal_b.id} "
                        f"takes precedence."
                    ),
                )

        return None

    def _same_base_metric(self, metric_a: str, metric_b: str) -> bool:
        """Check if two metrics refer to the same underlying measure."""
        base_a = metric_a.replace("reduce_", "").replace("increase_", "")
        base_b = metric_b.replace("reduce_", "").replace("increase_", "")
        return base_a == base_b

    def get_goal_tree(self) -> dict[str, Any]:
        """
        Get hierarchical representation of all goals.

        Returns:
            Tree structure of goals
        """
        # Find root goals (no parent)
        roots = [g for g in self.goals.values() if g.parent_goal_id is None]

        def build_tree(goal: Goal) -> dict[str, Any]:
            return {
                "id": goal.id,
                "name": goal.name,
                "level": goal.level.value,
                "progress": f"{goal.progress_percentage():.1f}%",
                "status": goal.status.value,
                "children": [
                    build_tree(self.goals[child_id])
                    for child_id in goal.child_goal_ids
                    if child_id in self.goals
                ],
            }

        return {"goals": [build_tree(root) for root in roots]}

    def get_statistics(self) -> dict[str, Any]:
        """
        Get statistics about goal progress.

        Returns:
            Dictionary of statistics
        """
        total = len(self.goals)
        achieved = sum(1 for g in self.goals.values() if g.status == GoalStatus.ACHIEVED)
        active = sum(1 for g in self.goals.values() if g.status == GoalStatus.ACTIVE)

        avg_progress = (
            sum(g.progress_percentage() for g in self.goals.values() if g.status == GoalStatus.ACTIVE)
            / active
            if active > 0
            else 0.0
        )

        return {
            "total_goals": total,
            "achieved_goals": achieved,
            "active_goals": active,
            "average_progress": avg_progress,
            "existential_goals": sum(
                1 for g in self.goals.values() if g.level == GoalLevel.EXISTENTIAL
            ),
            "conflicts_detected": len(self.detect_goal_conflicts()),
        }
