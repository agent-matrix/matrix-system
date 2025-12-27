"""
Intelligence modules for superintelligent capabilities.

This package provides the core intelligence capabilities including:
- Persistent memory and experience accumulation
- Meta-learning and adaptive strategies
- Goal hierarchy and multi-level objectives
- Pattern recognition and knowledge extraction
"""

from matrix_system.intelligence.goals import GoalHierarchy, GoalLevel
from matrix_system.intelligence.memory import Experience, MemoryStore, Pattern
from matrix_system.intelligence.meta_learning import MetaLearner, Strategy

__all__ = [
    "MemoryStore",
    "Experience",
    "Pattern",
    "MetaLearner",
    "Strategy",
    "GoalHierarchy",
    "GoalLevel",
]
