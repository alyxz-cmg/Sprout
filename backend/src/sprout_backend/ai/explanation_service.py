# backend/ai/explanation_service.py

from typing import Dict
from .client import generate_explanation
from ..schemas.explain import ExplainResponse


async def explain_translation(translation_data: Dict) -> ExplainResponse:
    """
    High-level service for generating explanations.

    Responsibilities:
    - Calls OpenAI client
    - Ensures a safe fallback
    - Keeps API layer clean
    """

    try:
        response = await generate_explanation(translation_data)

        # Defensive check (in case parsing fails silently)
        if not response or not response.explanations:
            return _fallback_response()

        return response

    except Exception:
        # Absolute safety net — never let AI break the app
        return _fallback_response()


def _fallback_response() -> ExplainResponse:
    """
    Safe fallback explanation if AI fails.
    """
    return ExplainResponse(
        explanations=[
            {
                "section": "Let’s Explore Your Code!",
                "text": (
                    "Your Scratch project was successfully turned into Python code! "
                    "Even though I couldn’t generate a full explanation right now, "
                    "you can still look at the code and try to spot patterns. "
                    "You're doing great—keep going!"
                ),
            }
        ]
    )