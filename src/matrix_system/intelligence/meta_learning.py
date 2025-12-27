"""
Meta-learning framework - learning how to learn.

This module implements meta-learning capabilities that allow the system
to analyze which strategies work best in which contexts and continuously
improve its learning process.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class StrategyType(str, Enum):
    """Types of learning strategies."""

    MODEL_SELECTION = "model_selection"  # Which AI model to use
    PROMPT_ENGINEERING = "prompt_engineering"  # How to phrase prompts
    HEALTH_CHECK = "health_check"  # Which health checks to use
    REMEDIATION = "remediation"  # How to fix problems
    PREDICTION = "prediction"  # How to predict failures


class Strategy(BaseModel):
    """
    A specific approach to solving a problem.

    Strategies are evaluated and ranked based on their performance
    across different contexts.
    """

    id: Optional[int] = Field(default=None, description="Unique strategy ID")
    name: str = Field(..., description="Name of the strategy")
    strategy_type: StrategyType = Field(..., description="Type of strategy")
    description: str = Field(..., description="What this strategy does")

    # Strategy definition
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters that define this strategy",
    )
    applicable_contexts: list[str] = Field(
        default_factory=list,
        description="Contexts where this strategy applies",
    )

    # Performance metrics
    times_used: int = Field(default=0, description="How many times used")
    success_count: int = Field(default=0, description="How many times successful")
    total_execution_time_ms: float = Field(default=0.0, description="Total execution time")

    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When strategy was created",
    )
    last_used: Optional[datetime] = Field(default=None, description="When last used")

    def success_rate(self) -> float:
        """Calculate success rate."""
        return (self.success_count / self.times_used) if self.times_used > 0 else 0.0

    def average_execution_time(self) -> float:
        """Calculate average execution time."""
        return (
            (self.total_execution_time_ms / self.times_used) if self.times_used > 0 else 0.0
        )


class StrategyRanking(BaseModel):
    """Ranking of strategies for a specific context."""

    context: str = Field(..., description="The context this ranking applies to")
    ranked_strategies: list[tuple[str, float]] = Field(
        ...,
        description="Strategies ranked by score (strategy_name, score)",
    )
    ranking_criteria: dict[str, float] = Field(
        default_factory=dict,
        description="Weights used for ranking",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When ranking was updated",
    )


class Problem(BaseModel):
    """A problem that needs to be solved."""

    problem_type: str = Field(..., description="Type of problem")
    context: dict[str, Any] = Field(..., description="Problem context")
    constraints: dict[str, Any] = Field(
        default_factory=dict,
        description="Constraints on solutions",
    )
    priority: str = Field(default="medium", description="Priority level")


class MetaLearner:
    """
    System that learns how to learn more effectively.

    This class analyzes which strategies work best in which contexts
    and continuously improves the learning process itself.
    """

    def __init__(self) -> None:
        """Initialize meta-learner."""
        self.strategies: dict[str, Strategy] = {}
        self.rankings: dict[str, StrategyRanking] = {}
        self._next_id = 1

        # Initialize with default strategies
        self._initialize_default_strategies()

    def _initialize_default_strategies(self) -> None:
        """Create default strategies."""
        default_strategies = [
            Strategy(
                id=1,
                name="gpt4_detailed_prompt",
                strategy_type=StrategyType.MODEL_SELECTION,
                description="Use GPT-4 with detailed, structured prompts",
                parameters={"model": "gpt-4", "prompt_style": "detailed"},
                applicable_contexts=["complex_analysis", "creative_problem_solving"],
            ),
            Strategy(
                id=2,
                name="claude_concise_prompt",
                strategy_type=StrategyType.MODEL_SELECTION,
                description="Use Claude with concise, direct prompts",
                parameters={"model": "claude", "prompt_style": "concise"},
                applicable_contexts=["simple_remediation", "quick_decisions"],
            ),
            Strategy(
                id=3,
                name="comprehensive_health_check",
                strategy_type=StrategyType.HEALTH_CHECK,
                description="Run all available health checks",
                parameters={"check_types": ["http", "mcp_echo", "resource_usage"]},
                applicable_contexts=["initial_diagnosis", "unknown_problem"],
            ),
            Strategy(
                id=4,
                name="targeted_health_check",
                strategy_type=StrategyType.HEALTH_CHECK,
                description="Run specific health checks based on symptoms",
                parameters={"adaptive": True},
                applicable_contexts=["known_problem_type", "performance_optimization"],
            ),
        ]

        for strategy in default_strategies:
            self.strategies[strategy.name] = strategy

        self._next_id = len(default_strategies) + 1

    def analyze_strategy_performance(
        self,
        context: str,
        criteria: Optional[dict[str, float]] = None,
    ) -> StrategyRanking:
        """
        Rank strategies by performance in a specific context.

        Args:
            context: The context to rank strategies for
            criteria: Weights for ranking (success_rate, speed, cost, etc.)

        Returns:
            Ranking of strategies for this context
        """
        # Default criteria weights
        if criteria is None:
            criteria = {
                "success_rate": 0.6,  # 60% weight on success
                "speed": 0.3,  # 30% weight on execution speed
                "reliability": 0.1,  # 10% weight on consistency
            }

        # Filter strategies applicable to this context
        applicable = [
            s for s in self.strategies.values() if context in s.applicable_contexts
        ]

        if not applicable:
            # Return empty ranking
            return StrategyRanking(
                context=context,
                ranked_strategies=[],
                ranking_criteria=criteria,
            )

        # Score each strategy
        scored_strategies: list[tuple[str, float]] = []
        for strategy in applicable:
            score = 0.0

            # Success rate component
            score += strategy.success_rate() * criteria.get("success_rate", 0.6)

            # Speed component (inverse of execution time, normalized)
            avg_time = strategy.average_execution_time()
            if avg_time > 0:
                speed_score = min(1000 / avg_time, 1.0)  # Normalize to 0-1
                score += speed_score * criteria.get("speed", 0.3)

            # Reliability component (based on times used)
            reliability_score = min(strategy.times_used / 100.0, 1.0)
            score += reliability_score * criteria.get("reliability", 0.1)

            scored_strategies.append((strategy.name, score))

        # Sort by score
        scored_strategies.sort(key=lambda x: x[1], reverse=True)

        ranking = StrategyRanking(
            context=context,
            ranked_strategies=scored_strategies,
            ranking_criteria=criteria,
        )

        self.rankings[context] = ranking
        return ranking

    def adapt_approach(self, context: str) -> Optional[Strategy]:
        """
        Select optimal strategy based on past performance.

        Args:
            context: Current context

        Returns:
            Best strategy for this context, or None if no applicable strategy
        """
        # Get or create ranking for this context
        if context not in self.rankings:
            self.analyze_strategy_performance(context)

        ranking = self.rankings.get(context)
        if not ranking or not ranking.ranked_strategies:
            return None

        # Return highest ranked strategy
        best_strategy_name = ranking.ranked_strategies[0][0]
        return self.strategies.get(best_strategy_name)

    def propose_new_strategy(self, problem: Problem) -> Strategy:
        """
        Generate a novel strategy by combining successful patterns.

        Args:
            problem: The problem to solve

        Returns:
            New strategy created by combining existing successful strategies
        """
        # Find successful strategies
        successful = [
            s for s in self.strategies.values() if s.success_rate() > 0.7 and s.times_used > 5
        ]

        if not successful:
            # Create basic strategy
            return Strategy(
                id=self._next_id,
                name=f"basic_strategy_{self._next_id}",
                strategy_type=StrategyType.REMEDIATION,
                description=f"Basic approach for {problem.problem_type}",
                parameters={"problem_type": problem.problem_type},
                applicable_contexts=[problem.problem_type],
            )

        # Combine parameters from successful strategies
        combined_params: dict[str, Any] = {}
        for strategy in successful[:3]:  # Use top 3
            combined_params.update(strategy.parameters)

        # Create new hybrid strategy
        new_strategy = Strategy(
            id=self._next_id,
            name=f"hybrid_strategy_{self._next_id}",
            strategy_type=StrategyType.REMEDIATION,
            description=f"Hybrid approach combining {len(successful[:3])} successful strategies",
            parameters=combined_params,
            applicable_contexts=[problem.problem_type],
        )

        self._next_id += 1
        self.strategies[new_strategy.name] = new_strategy

        return new_strategy

    def update_strategy_performance(
        self,
        strategy_name: str,
        success: bool,
        execution_time_ms: float,
    ) -> None:
        """
        Update performance metrics for a strategy.

        Args:
            strategy_name: Name of the strategy used
            success: Whether it succeeded
            execution_time_ms: How long it took
        """
        if strategy_name not in self.strategies:
            return

        strategy = self.strategies[strategy_name]
        strategy.times_used += 1
        if success:
            strategy.success_count += 1
        strategy.total_execution_time_ms += execution_time_ms
        strategy.last_used = datetime.utcnow()

        # Invalidate rankings that include this strategy
        for context in list(self.rankings.keys()):
            if context in strategy.applicable_contexts:
                del self.rankings[context]

    def get_learning_insights(self) -> dict[str, Any]:
        """
        Get insights about the learning process.

        Returns:
            Dictionary of meta-learning insights
        """
        total_strategies = len(self.strategies)
        successful_strategies = sum(
            1 for s in self.strategies.values() if s.success_rate() > 0.7
        )

        avg_success_rate = (
            sum(s.success_rate() for s in self.strategies.values()) / total_strategies
            if total_strategies > 0
            else 0.0
        )

        return {
            "total_strategies": total_strategies,
            "successful_strategies": successful_strategies,
            "average_success_rate": avg_success_rate,
            "contexts_analyzed": len(self.rankings),
            "most_successful_strategy": self._get_most_successful_strategy(),
            "fastest_strategy": self._get_fastest_strategy(),
        }

    def _get_most_successful_strategy(self) -> str:
        """Get the name of the most successful strategy."""
        if not self.strategies:
            return "none"

        best = max(
            self.strategies.values(),
            key=lambda s: (s.success_rate(), s.times_used),
        )
        return f"{best.name} ({best.success_rate():.1%} success)"

    def _get_fastest_strategy(self) -> str:
        """Get the name of the fastest strategy."""
        if not self.strategies:
            return "none"

        strategies_with_data = [s for s in self.strategies.values() if s.times_used > 0]
        if not strategies_with_data:
            return "none"

        fastest = min(
            strategies_with_data,
            key=lambda s: s.average_execution_time(),
        )
        return f"{fastest.name} ({fastest.average_execution_time():.0f}ms avg)"
