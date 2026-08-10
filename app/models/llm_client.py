import os
from typing import Optional

# Lazy initialize OpenAI client only when needed
_client = None

def get_client():
    """Get or initialize OpenAI client"""
    global _client
    if _client is None:
        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set in environment")
            _client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package not installed")
    return _client


def call_llm(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Call OpenAI LLM and return response text.

    Args:
        prompt: User input/question
        model: Model to use (default: gpt-3.5-turbo)

    Returns:
        Response text from the model
    """
    try:
        client = get_client()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling LLM: {str(e)}"
