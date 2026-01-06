def evaluate_confidence(response_text: str) -> str:
    """
    Very simple confidence check.
    This is a temporary stub.
    """

    unsure_words = [
        "might",
        "maybe",
        "not sure",
        "possibly",
        "could be",
        "uncertain"
    ]

    for word in unsure_words:
        if word in response_text.lower():
            return "guessing"

    return "confident"

