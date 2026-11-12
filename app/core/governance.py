"""
Governance layer for Sentinel.

Tracks system-level behavior, enforces usage policies, and provides
auditable decision records. Governance is separate from UX — users
don't control or see this layer directly.
"""

from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict


class GovernanceEngine:
    """
    Tracks usage patterns and enforces governance rules.

    Primary concerns:
    - Overconfidence rate: how often the system is confidently wrong
    - Correction acceptance: how the system responds to corrections
    - Usage drift: detecting when usage patterns shift toward misuse
    - Policy compliance: ensuring safety rules are consistently applied
    """

    def __init__(self):
        self.session_records: Dict[str, List[Dict]] = defaultdict(list)
        self.global_stats = {
            "total_interactions": 0,
            "total_corrections": 0,
            "total_safety_flags": 0,
            "overconfidence_events": 0,
            "sessions_created": 0,
        }

    def record_interaction(
        self,
        session_id: str,
        confidence_score: float,
        confidence_level: str,
        safety_flags: List[str] = None,
        was_corrected: bool = False,
    ) -> None:
        """Record a single LLM interaction for governance tracking."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "confidence_score": confidence_score,
            "confidence_level": confidence_level,
            "safety_flags": safety_flags or [],
            "was_corrected": was_corrected,
        }
        self.session_records[session_id].append(entry)
        self.global_stats["total_interactions"] += 1

        if safety_flags:
            self.global_stats["total_safety_flags"] += len(safety_flags)

        if confidence_level == "confident" and was_corrected:
            self.global_stats["overconfidence_events"] += 1

    def record_correction(self, session_id: str) -> None:
        """Flag the last interaction in a session as corrected."""
        self.global_stats["total_corrections"] += 1
        records = self.session_records.get(session_id, [])
        if records:
            records[-1]["was_corrected"] = True

    def get_session_governance_report(self, session_id: str) -> Dict:
        """
        Generate a governance report for a session.
        Flags: high overconfidence rate, frequent safety flags, etc.
        """
        records = self.session_records.get(session_id, [])
        if not records:
            return {"session_id": session_id, "status": "no data"}

        total = len(records)
        corrected = sum(1 for r in records if r["was_corrected"])
        confident_wrong = sum(
            1 for r in records
            if r["confidence_level"] == "confident" and r["was_corrected"]
        )
        safety_flagged = sum(1 for r in records if r["safety_flags"])

        overconfidence_rate = confident_wrong / total if total > 0 else 0.0

        flags = []
        if overconfidence_rate > 0.3:
            flags.append("high_overconfidence_rate")
        if safety_flagged / total > 0.2:
            flags.append("frequent_safety_flags")
        if corrected / total > 0.5:
            flags.append("high_correction_rate")

        return {
            "session_id": session_id,
            "total_interactions": total,
            "total_corrected": corrected,
            "overconfidence_rate": round(overconfidence_rate, 2),
            "safety_flagged_count": safety_flagged,
            "governance_flags": flags,
            "status": "flagged" if flags else "clean",
        }

    def get_global_report(self) -> Dict:
        """System-wide governance summary."""
        total = self.global_stats["total_interactions"]
        return {
            **self.global_stats,
            "overconfidence_rate": round(
                self.global_stats["overconfidence_events"] / total, 2
            ) if total > 0 else 0.0,
            "correction_rate": round(
                self.global_stats["total_corrections"] / total, 2
            ) if total > 0 else 0.0,
            "generated_at": datetime.now().isoformat(),
        }


# Global governance engine instance
governance_engine = GovernanceEngine()
