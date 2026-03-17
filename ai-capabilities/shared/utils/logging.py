"""Logging utilities."""

import sys
import logging
import structlog
from typing import Any, Dict


def setup_logging(log_level: str = "INFO", log_format: str = "json") -> None:
    """Configure structured logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Output format ("json" or "console")
    """
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if log_format == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str, **context: Any) -> structlog.BoundLogger:
    """Get a structured logger instance.

    Args:
        name: Logger name (typically __name__)
        **context: Additional context to bind to logger

    Returns:
        Structured logger instance
    """
    logger = structlog.get_logger(name)
    if context:
        logger = logger.bind(**context)
    return logger
