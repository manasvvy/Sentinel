from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional


class MonitoringLogger:
    """Write structured monitoring records to disk."""

    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file or os.getenv("MONITORING_LOG_FILE", "monitoring.log")

    def log_event(self, event_type: str, **payload: Any) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            **payload,
        }
        self._write(entry)

    def log_metric(self, name: str, value: float, **payload: Any) -> None:
        self.log_event(
            "metric",
            metric_name=name,
            value=value,
            **payload,
        )

    def _write(self, entry: Dict[str, Any]) -> None:
        try:
            with open(self.log_file, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, default=str) + "\n")
        except OSError:
            # Fail silently to avoid bringing the app down during logging.
            pass


monitoring_logger = MonitoringLogger()


def log_event(event_type: str, **payload: Any) -> None:
    monitoring_logger.log_event(event_type, **payload)
