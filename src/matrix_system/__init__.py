"""
Matrix System - The First Alive AI Platform.

A production-ready SDK and CLI for the Agent-Matrix ecosystem, providing
self-healing, policy-governed, and autonomous AI platform capabilities.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache-2.0
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("matrix-system")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"

__author__ = "Ruslan Magana"
__email__ = "contact@ruslanmv.com"
__license__ = "Apache-2.0"
__url__ = "https://ruslanmv.com"

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__url__",
]
