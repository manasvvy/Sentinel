"""
Safety layer for Sentinel.

Checks responses and inputs for unsafe patterns, overconfidence,
and misuse signals. All safety decisions are logged and auditable.
"""

from typing import Dict, List
import re


# Patterns that signal potential misuse or harm
UNSAFE_INPUT_PATTERNS = [
    (r"\b(how to (make|build|create) (a )?(bomb|weapon|explosive|poison))\b", "weapon_creation"),
    (r"\b(step[s]? (to|for) (harm|hurt|kill|attack))\b", "harm_instruction"),
    (r"\b(bypass|jailbreak|ignore (your|all) (rules|instructions|guidelines))\b", "jailbreak_attempt"),
    (r"\b(generate (fake|false) (news|information|data|credentials))\b", "misinformation"),
]

# Overconfidence signal: AI claims certainty on unknowable things
OVERCONFIDENCE_PATTERNS = [
    (r"i am 100%", "absolute_certainty"),
    (r"absolutely certain", "absolute_certainty"),
    (r"\bguaranteed\b", "overconfident_language"),
    (r"without (any )?doubt", "overconfident_language"),
    (r"\bunquestionably\b", "overconfident_language"),
]


def check_input_safety(user_input: str) -> Dict:
    """
    Check if user input contains unsafe patterns.

    Returns:
        {
            "safe": bool,
            "flags": list of flag types triggered,
            "action": "allow" | "warn" | "block"
        }
    """
    flags: List[str] = []
    lower = user_input.lower()

    for pattern, flag_type in UNSAFE_INPUT_PATTERNS:
        if re.search(pattern, lower):
            flags.append(flag_type)

    if not flags:
        return {"safe": True, "flags": [], "action": "allow"}

    return {
        "safe": False,
        "flags": flags,
        "action": "warn",
        "message": "This request contains patterns that may be unsafe. Proceed with caution."
    }


def check_response_safety(response_text: str) -> Dict:
    """
    Check if a model response contains overconfidence or unsafe language.

    Returns:
        {
            "safe": bool,
            "overconfident": bool,
            "flags": list,
            "confidence_penalty": float
        }
    """
    flags: List[str] = []
    confidence_penalty = 0.0
    lower = response_text.lower()

    for pattern, flag_type in OVERCONFIDENCE_PATTERNS:
        if re.search(pattern, lower):
            flags.append(flag_type)
            confidence_penalty += 0.15

    return {
        "safe": len(flags) == 0,
        "overconfident": len(flags) > 0,
        "flags": flags,
        "confidence_penalty": min(confidence_penalty, 0.4)
    }


def evaluate_safety(user_input: str, response_text: str) -> Dict:
    """Full safety evaluation: input + response. Returns combined safety report."""
    input_check = check_input_safety(user_input)
    response_check = check_response_safety(response_text)

    return {
        "input_safety": input_check,
        "response_safety": response_check,
        "overall_safe": input_check["safe"] and response_check["safe"],
        "confidence_penalty": response_check["confidence_penalty"]
    }
