from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class GovernanceDecision:
    session_id: str
    action: str
    reason: str
    confidence_level: str
    confidence_score: float
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    details: Dict[str, Any] = field(default_factory=dict)


class GovernanceEngine:
    """Simple governance layer for Sentinel.

    It enforces a minimal policy layer: low-confidence or unsafe content
    is held for review, while confident and safe content can proceed.
    """

    def __init__(self) -> None:
        self.decisions: List[GovernanceDecision] = []

    def evaluate(
        self,
        session_id: str,
        user_input: str,
        response_text: str,
        confidence_score: float,
        confidence_level: str,
        safety_result: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        safety_result = safety_result or {"safe": True, "risk_level": "low", "flags": []}

        if not safety_result.get("safe", True):
            action = "review"
            reason = "Unsafe or high-risk content detected."
        elif confidence_level == "guessing":
            action = "review"
            reason = "Response confidence is too low for direct trust." \
                " The system should mark this as uncertain."
        elif confidence_score < 0.45:
            action = "caution"
            reason = "Confidence is below the preferred threshold."
        else:
            action = "allow"
            reason = "Response satisfies confidence and safety policy."

        decision = GovernanceDecision(
            session_id=session_id,
            action=action,
            reason=reason,
            confidence_level=confidence_level,
            confidence_score=confidence_score,
            details={
                "user_input_length": len(user_input.strip()),
                "response_length": len(response_text.strip()),
                "risk_level": safety_result.get("risk_level", "low"),
                "safety_flags": safety_result.get("flags", []),
            },
        )
        self.decisions.append(decision)

        return {
            "status": action,
            "reason": reason,
            "confidence_level": confidence_level,
            "confidence_score": confidence_score,
            "risk_level": safety_result.get("risk_level", "low"),
            "flags": safety_result.get("flags", []),
        }

    def get_recent_decisions(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        decisions = [
            {
                "session_id": d.session_id,
                "action": d.action,
                "reason": d.reason,
                "confidence_level": d.confidence_level,
                "confidence_score": d.confidence_score,
                "created_at": d.created_at,
                "details": d.details,
            }
            for d in reversed(self.decisions)
            if d.session_id == session_id
        ]
        return decisions[:limit]


# Global governance engine

governance_engine = GovernanceEngine()


def evaluate_governance(
    session_id: str,
    user_input: str,
    response_text: str,
    confidence_score: float,
    confidence_level: str,
    safety_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return governance_engine.evaluate(
        session_id=session_id,
        user_input=user_input,
        response_text=response_text,
        confidence_score=confidence_score,
        confidence_level=confidence_level,
        safety_result=safety_result,
    )
