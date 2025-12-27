"""
Ethical framework for Matrix System superintelligence.

This module provides immutable ethical constraints and decision-making
frameworks that govern all autonomous system behavior.
"""

from matrix_system.ethics.core import EthicalCore, EthicalViolationError
from matrix_system.ethics.decision import EthicalDecisionMaker, EthicalFramework
from matrix_system.ethics.transparency import TransparencyEngine, AuditLevel

__all__ = [
    "EthicalCore",
    "EthicalViolationError",
    "EthicalDecisionMaker",
    "EthicalFramework",
    "TransparencyEngine",
    "AuditLevel",
]
