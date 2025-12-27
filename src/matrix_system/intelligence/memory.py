"""
Persistent memory system for experience accumulation.

This module implements a hierarchical memory system that allows the system
to learn from experience, recognize patterns, and improve over time.

Memory Layers:
- Working Memory: Current context and active information
- Episodic Memory: Past experiences with outcomes
- Semantic Memory: Learned patterns and knowledge
- Procedural Memory: Skills and capabilities
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    """Types of memory storage."""

    WORKING = "working"  # Short-term active memory
    EPISODIC = "episodic"  # Specific experiences
    SEMANTIC = "semantic"  # General knowledge/patterns
    PROCEDURAL = "procedural"  # How to do things


class OutcomeType(str, Enum):
    """Outcome classification for experiences."""

    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    UNKNOWN = "unknown"


class Experience(BaseModel):
    """
    Represents a single experience with context and outcome.

    This is the fundamental unit of learning in the memory system.
    """

    id: Optional[int] = Field(default=None, description="Unique experience ID")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this experience occurred",
    )

    # Context
    situation: dict[str, Any] = Field(..., description="The situation encountered")
    problem_type: str = Field(..., description="Type of problem faced")
    context_features: dict[str, Any] = Field(
        default_factory=dict,
        description="Key features of the context",
    )

    # Action taken
    action_type: str = Field(..., description="What action was taken")
    action_parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters of the action",
    )
    strategy_used: str = Field(..., description="Strategy that guided the action")

    # Outcome
    outcome: OutcomeType = Field(..., description="How it turned out")
    outcome_details: dict[str, Any] = Field(
        default_factory=dict,
        description="Detailed outcome information",
    )
    success_metrics: dict[str, float] = Field(
        default_factory=dict,
        description="Measurable outcomes",
    )

    # Learning
    lessons_learned: list[str] = Field(
        default_factory=list,
        description="What was learned from this",
    )
    confidence_score: float = Field(
        default=0.5,
        description="Confidence in this experience's reliability",
        ge=0.0,
        le=1.0,
    )

    # Retrieval metadata
    retrieval_count: int = Field(default=0, description="How many times this was retrieved")
    last_retrieved: Optional[datetime] = Field(
        default=None,
        description="When this was last used",
    )


class Pattern(BaseModel):
    """
    A recognized pattern extracted from multiple experiences.

    Patterns represent generalized knowledge that can be applied
    to new situations.
    """

    id: Optional[int] = Field(default=None, description="Unique pattern ID")
    pattern_type: str = Field(..., description="Type of pattern")
    description: str = Field(..., description="Human-readable description")

    # Pattern definition
    preconditions: dict[str, Any] = Field(..., description="When this pattern applies")
    recommended_action: str = Field(..., description="What to do when pattern matches")
    expected_outcome: str = Field(..., description="What usually happens")

    # Evidence
    supporting_experiences: list[int] = Field(
        default_factory=list,
        description="IDs of experiences that support this pattern",
    )
    confidence: float = Field(
        default=0.0,
        description="Statistical confidence in pattern",
        ge=0.0,
        le=1.0,
    )
    success_rate: float = Field(
        default=0.0,
        description="Success rate when pattern is followed",
        ge=0.0,
        le=1.0,
    )

    # Metadata
    discovered_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When pattern was discovered",
    )
    times_applied: int = Field(default=0, description="How many times used")
    last_applied: Optional[datetime] = Field(default=None, description="When last used")


class Context(BaseModel):
    """Current context for memory retrieval."""

    problem_type: str = Field(..., description="Type of problem")
    features: dict[str, Any] = Field(..., description="Context features")
    similarity_threshold: float = Field(
        default=0.7,
        description="Minimum similarity for retrieval",
        ge=0.0,
        le=1.0,
    )


class MemoryStore:
    """
    Hierarchical memory system for experience accumulation.

    This class manages the storage, retrieval, and consolidation of
    experiences and patterns learned by the system.
    """

    def __init__(self) -> None:
        """Initialize memory store."""
        self.working_memory: list[Experience] = []
        self.episodic_memory: list[Experience] = []
        self.semantic_memory: list[Pattern] = []
        self._next_experience_id = 1
        self._next_pattern_id = 1

    def store_experience(self, experience: Experience) -> None:
        """
        Store a new experience in working memory.

        Args:
            experience: The experience to store
        """
        experience.id = self._next_experience_id
        self._next_experience_id += 1
        self.working_memory.append(experience)

        # Auto-consolidate if working memory gets too large
        if len(self.working_memory) > 100:
            self.consolidate()

    def retrieve_similar(self, context: Context, limit: int = 5) -> list[Experience]:
        """
        Retrieve similar past experiences.

        Args:
            context: The current context
            limit: Maximum number of experiences to return

        Returns:
            List of similar experiences, sorted by relevance
        """
        # Combine episodic and working memory
        all_experiences = self.episodic_memory + self.working_memory

        # Filter by problem type
        relevant = [e for e in all_experiences if e.problem_type == context.problem_type]

        # Calculate similarity scores
        scored_experiences = [
            (exp, self._calculate_similarity(exp, context)) for exp in relevant
        ]

        # Filter by threshold and sort
        filtered = [
            (exp, score)
            for exp, score in scored_experiences
            if score >= context.similarity_threshold
        ]
        filtered.sort(key=lambda x: x[1], reverse=True)

        # Update retrieval metadata
        for exp, _ in filtered[:limit]:
            exp.retrieval_count += 1
            exp.last_retrieved = datetime.utcnow()

        return [exp for exp, _ in filtered[:limit]]

    def consolidate(self) -> None:
        """
        Move experiences from working memory to long-term episodic memory.

        This process also triggers pattern extraction.
        """
        # Move successful experiences to episodic memory
        for exp in self.working_memory:
            if exp.outcome in [OutcomeType.SUCCESS, OutcomeType.PARTIAL_SUCCESS]:
                self.episodic_memory.append(exp)

        # Clear working memory
        self.working_memory.clear()

        # Extract new patterns
        new_patterns = self.extract_patterns()
        self.semantic_memory.extend(new_patterns)

    def extract_patterns(self) -> list[Pattern]:
        """
        Identify recurring successful patterns from experiences.

        Returns:
            List of newly discovered patterns
        """
        patterns: list[Pattern] = []

        # Group experiences by problem type
        by_problem_type: dict[str, list[Experience]] = {}
        for exp in self.episodic_memory:
            if exp.problem_type not in by_problem_type:
                by_problem_type[exp.problem_type] = []
            by_problem_type[exp.problem_type].append(exp)

        # Find patterns within each problem type
        for problem_type, experiences in by_problem_type.items():
            # Need at least 3 similar experiences to form a pattern
            if len(experiences) < 3:
                continue

            # Group by strategy
            by_strategy: dict[str, list[Experience]] = {}
            for exp in experiences:
                if exp.strategy_used not in by_strategy:
                    by_strategy[exp.strategy_used] = []
                by_strategy[exp.strategy_used].append(exp)

            # Create patterns for successful strategies
            for strategy, strategy_exps in by_strategy.items():
                success_count = sum(
                    1 for e in strategy_exps if e.outcome == OutcomeType.SUCCESS
                )
                success_rate = success_count / len(strategy_exps)

                if success_rate >= 0.7:  # 70% success rate threshold
                    pattern = Pattern(
                        id=self._next_pattern_id,
                        pattern_type=f"{problem_type}_{strategy}",
                        description=f"When facing {problem_type}, use {strategy}",
                        preconditions={"problem_type": problem_type},
                        recommended_action=strategy,
                        expected_outcome=f"Success rate: {success_rate:.1%}",
                        supporting_experiences=[e.id for e in strategy_exps if e.id],
                        confidence=min(len(strategy_exps) / 10.0, 1.0),
                        success_rate=success_rate,
                    )
                    self._next_pattern_id += 1
                    patterns.append(pattern)

        return patterns

    def get_best_pattern(self, context: Context) -> Optional[Pattern]:
        """
        Get the best matching pattern for a context.

        Args:
            context: Current context

        Returns:
            Best matching pattern if one exists
        """
        # Filter patterns by problem type
        matching = [
            p
            for p in self.semantic_memory
            if p.preconditions.get("problem_type") == context.problem_type
        ]

        if not matching:
            return None

        # Sort by success rate and confidence
        matching.sort(key=lambda p: (p.success_rate, p.confidence), reverse=True)
        return matching[0]

    def _calculate_similarity(self, experience: Experience, context: Context) -> float:
        """
        Calculate similarity between experience and context.

        Args:
            experience: Past experience
            context: Current context

        Returns:
            Similarity score (0-1)
        """
        # Simple similarity based on matching features
        common_keys = set(experience.context_features.keys()) & set(context.features.keys())

        if not common_keys:
            return 0.0

        matches = sum(
            1
            for key in common_keys
            if experience.context_features[key] == context.features[key]
        )

        return matches / len(common_keys)

    def get_statistics(self) -> dict[str, Any]:
        """
        Get memory system statistics.

        Returns:
            Dictionary of statistics
        """
        total_experiences = len(self.episodic_memory) + len(self.working_memory)
        successful = sum(
            1
            for e in self.episodic_memory + self.working_memory
            if e.outcome == OutcomeType.SUCCESS
        )

        return {
            "working_memory_size": len(self.working_memory),
            "episodic_memory_size": len(self.episodic_memory),
            "patterns_discovered": len(self.semantic_memory),
            "total_experiences": total_experiences,
            "success_rate": (successful / total_experiences) if total_experiences > 0 else 0.0,
            "average_pattern_confidence": (
                sum(p.confidence for p in self.semantic_memory) / len(self.semantic_memory)
                if self.semantic_memory
                else 0.0
            ),
        }

    def prune_old_experiences(self, days: int = 90) -> int:
        """
        Remove experiences older than specified days.

        Args:
            days: Age threshold in days

        Returns:
            Number of experiences removed
        """
        cutoff = datetime.utcnow() - timedelta(days=days)
        original_count = len(self.episodic_memory)

        self.episodic_memory = [
            e for e in self.episodic_memory if e.timestamp >= cutoff or e.retrieval_count > 10
        ]

        return original_count - len(self.episodic_memory)
