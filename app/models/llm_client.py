import os
from openai import OpenAI
from typing import Optional

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling LLM: {str(e)}"
