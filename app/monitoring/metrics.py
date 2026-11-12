"""
Metrics collection for Sentinel monitoring.

Tracks system-level performance and behavioral metrics.
Lightweight in-memory store — no external dependencies.
"""

from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict
import statistics


class MetricsCollector:
    """
    Collects and aggregates system metrics.

    Tracks:
    - Response latency
    - Confidence distribution over time
    - Correction patterns
    - Safety flag frequency
    - Session activity
    """

    def __init__(self):
        self._latencies: List[float] = []
        self._confidence_scores: List[float] = []
        self._confidence_levels: Dict[str, int] = defaultdict(int)
        self._correction_count: int = 0
        self._interaction_count: int = 0
        self._safety_flag_count: int = 0
        self._error_count: int = 0
        self._session_count: int = 0
        self._hourly_interactions: Dict[str, int] = defaultdict(int)

    def record_interaction(
        self,
        confidence_score: float,
        confidence_level: str,
        latency_ms: Optional[float] = None,
    ) -> None:
        """Record a single LLM interaction."""
        self._interaction_count += 1
        self._confidence_scores.append(confidence_score)
        self._confidence_levels[confidence_level] += 1

        if latency_ms is not None:
            self._latencies.append(latency_ms)

        hour_key = datetime.now().strftime("%Y-%m-%dT%H")
        self._hourly_interactions[hour_key] += 1

    def record_correction(self) -> None:
        """Record a user correction."""
        self._correction_count += 1

    def record_safety_flag(self) -> None:
        """Record a safety flag event."""
        self._safety_flag_count += 1

    def record_error(self) -> None:
        """Record a system error."""
        self._error_count += 1

    def record_session_created(self) -> None:
        """Record a new session."""
        self._session_count += 1

    def get_summary(self) -> Dict:
        """Return current metrics summary."""
        avg_confidence = (
            round(statistics.mean(self._confidence_scores), 2)
            if self._confidence_scores else 0.0
        )
        p95_latency = None
        avg_latency = None
        if self._latencies:
            sorted_latencies = sorted(self._latencies)
            p95_idx = int(len(sorted_latencies) * 0.95)
            p95_latency = round(sorted_latencies[p95_idx], 1)
            avg_latency = round(statistics.mean(self._latencies), 1)

        correction_rate = (
            round(self._correction_count / self._interaction_count, 2)
            if self._interaction_count > 0 else 0.0
        )

        return {
            "total_interactions": self._interaction_count,
            "total_corrections": self._correction_count,
            "total_safety_flags": self._safety_flag_count,
            "total_errors": self._error_count,
            "total_sessions": self._session_count,
            "correction_rate": correction_rate,
            "avg_confidence_score": avg_confidence,
            "confidence_distribution": dict(self._confidence_levels),
            "avg_latency_ms": avg_latency,
            "p95_latency_ms": p95_latency,
            "generated_at": datetime.now().isoformat(),
        }

    def get_confidence_trend(self, last_n: int = 20) -> List[float]:
        """Return the last N confidence scores."""
        return self._confidence_scores[-last_n:]


# Global metrics collector
metrics = MetricsCollector()
