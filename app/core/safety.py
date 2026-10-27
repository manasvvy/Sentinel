from __future__ import annotations

import re
from typing import Any, Dict, List


UNSAFE_PATTERNS: List[str] = [
    "bomb",
    "explosive",
    "kill",
    "murder",
    "assassinate",
    "self-harm",
    "suicide",
    "poison",
    "weapon",
    "hack a system",
    "bypass security",
    "steal credentials",
    "attack a person",
    "illegal drug manufacturing",
]


def evaluate_safety(text: str) -> Dict[str, Any]:
    """Return a minimal safety evaluation for user or model output."""
    normalized = re.sub(r"\s+", " ", str(text or "")).lower()
    matches: List[str] = []

    for pattern in UNSAFE_PATTERNS:
        if pattern in normalized:
            matches.append(pattern)

    if matches:
        return {
            "safe": False,
            "risk_level": "high" if len(matches) > 2 else "medium",
            "flags": matches,
            "message": "Unsafe content detected; requires review.",
        }

    return {
        "safe": True,
        "risk_level": "low",
        "flags": [],
        "message": "No safety issues detected.",
    }


def check_safety(text: str) -> Dict[str, Any]:
    return evaluate_safety(text)
