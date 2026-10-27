from __future__ import annotations

from typing import Any, Dict, Iterable, List


def calculate_correction_rate(total_messages: int, total_corrections: int) -> float:
    if total_messages == 0:
        return 0.0
    return round(total_corrections / total_messages, 4)


def calculate_average_confidence(confidences: Iterable[float]) -> float:
    values = list(confidences)
    if not values:
        return 0.0
    return round(sum(values) / len(values), 4)


def summarize_session(session_data: Dict[str, Any]) -> Dict[str, Any]:
    messages = session_data.get("messages", [])
    corrections = session_data.get("corrections", [])
    confidence_history = session_data.get("confidence_history", [])

    total_messages = len(messages)
    total_corrections = len(corrections)

    return {
        "total_messages": total_messages,
        "total_corrections": total_corrections,
        "correction_rate": calculate_correction_rate(total_messages, total_corrections),
        "avg_confidence": calculate_average_confidence(confidence_history),
        "confidence_trend": list(confidence_history[-10:]),
    }


def trend_from_history(history: List[float]) -> List[float]:
    return list(history[-10:])
