"""
Structured logging for Sentinel monitoring.

Provides a structured log handler that emits JSON lines to stdout
(for cloud log aggregators) and optionally to a file.

This is separate from the audit logger in app/core/logging.py —
this is for operational/debugging logs, not governance audit trails.
"""

import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional


class JSONFormatter(logging.Formatter):
    """Format log records as JSON lines for log aggregation."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Include any extra fields attached to the record
        for key, value in record.__dict__.items():
            if key not in (
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "exc_info", "exc_text", "stack_info",
                "lineno", "funcName", "created", "msecs", "relativeCreated",
                "thread", "threadName", "processName", "process", "message",
            ):
                try:
                    json.dumps(value)  # Only include JSON-serializable values
                    log_entry[key] = value
                except (TypeError, ValueError):
                    log_entry[key] = str(value)

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def get_sentinel_logger(name: str = "sentinel") -> logging.Logger:
    """
    Get a structured logger for Sentinel.

    Logs to stdout as JSON (compatible with Render/cloud log drains).
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Already configured

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Stdout handler (JSON)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(JSONFormatter())
    logger.addHandler(stdout_handler)

    # Optional file handler (for local dev)
    log_file = os.getenv("LOG_FILE")
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(JSONFormatter())
            logger.addHandler(file_handler)
        except OSError:
            pass  # Don't crash if log file can't be opened

    logger.propagate = False
    return logger


def log_event(
    logger: logging.Logger,
    event_type: str,
    session_id: Optional[str] = None,
    **kwargs: Any,
) -> None:
    """Helper to log a structured event with extra fields."""
    extra = {"event_type": event_type}
    if session_id:
        extra["session_id"] = session_id
    extra.update(kwargs)
    logger.info(event_type, extra=extra)


# Module-level default logger
sentinel_logger = get_sentinel_logger("sentinel")
