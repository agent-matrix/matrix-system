"""
Logging utilities for Matrix System.

This module provides structured logging configuration using structlog
for consistent, production-ready logging across the application.
"""

import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, Processor


def add_log_level(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """
    Add log level to the event dictionary.

    Args:
        logger: Logger instance
        method_name: Name of the logging method called
        event_dict: Event dictionary to modify

    Returns:
        Modified event dictionary with log level
    """
    if method_name == "warn":
        method_name = "warning"
    event_dict["level"] = method_name.upper()
    return event_dict


def setup_logging(log_level: str = "INFO", json_format: bool = False) -> None:
    """
    Configure structured logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: If True, use JSON format for logs, otherwise use console format

    Raises:
        ValueError: If an invalid log level is provided
    """
    level = getattr(logging, log_level.upper(), None)
    if not isinstance(level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if json_format:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger instance.

    Args:
        name: Name for the logger (typically __name__)

    Returns:
        Configured structured logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("application_started", version="1.0.0")
    """
    return structlog.get_logger(name)
