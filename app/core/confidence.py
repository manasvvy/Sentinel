from typing import Dict, List


def evaluate_confidence(response_text: str, metadata: dict = None) -> Dict:
    """
    Evaluate confidence based on:
    - Language uncertainty signals
    - Citation/evidence availability
    - Response structure and completeness
    
    Returns a dict with score, level, and reasoning.
    """
    confidence_score = 0.7  # Start at baseline
    reasoning: List[str] = []
    
    # Explicit uncertainty markers (reduce confidence)
    uncertainty_signals = [
        ("might", 0.15),
        ("maybe", 0.15),
        ("possibly", 0.1),
        ("i'm not sure", 0.25),
        ("i don't know", 0.3),
        ("uncertain", 0.2),
        ("could be", 0.1),
        ("appears to", 0.05),
        ("seems to", 0.05),
        ("might be", 0.15),
    ]
    
    for signal, penalty in uncertainty_signals:
        if signal.lower() in response_text.lower():
            confidence_score -= penalty
            reasoning.append(f"Uncertainty marker found: '{signal}'")
    
    # Evidence/citations increase confidence
    if any(bracket in response_text for bracket in ["[", "]"]):
        if "[" in response_text and "]" in response_text:
            confidence_score += 0.15
            reasoning.append("Response includes citations/evidence")
    
    # Check for multiple sources of reasoning (increases confidence)
    if response_text.count("because") > 1 or response_text.count("reason") > 0:
        confidence_score += 0.1
        reasoning.append("Multiple reasoning paths present")
    
    # Normalize to 0-1 range
    confidence_score = max(0.0, min(1.0, confidence_score))
    
    # Determine confidence level
    if confidence_score >= 0.7:
        level = "confident"
    elif confidence_score >= 0.4:
        level = "cautious"
    else:
        level = "guessing"
    
    return {
        "score": round(confidence_score, 2),
        "level": level,
        "reasoning": reasoning if reasoning else ["Standard confidence baseline applied"]
    }
