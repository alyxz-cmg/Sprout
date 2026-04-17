import pytest
from unittest.mock import AsyncMock

from ai.explanation_service import explain_translation
from schemas.explain import ExplainResponse


# --- Sample input ---

SAMPLE_TRANSLATION = {
    "python_code": "print('hello')",
    "warnings": [],
    "mappings": []
}


# --- TESTS ---


@pytest.mark.asyncio
async def test_explanation_success(monkeypatch):
    """
    Service should return valid ExplainResponse when OpenAI succeeds.
    """

    mock_response = ExplainResponse(
        explanations=[
            {
                "section": "What this does",
                "text": "This prints hello!"
            }
        ]
    )

    async_mock = AsyncMock(return_value=mock_response)

    monkeypatch.setattr(
        "ai.explanation_service.generate_explanation",
        async_mock
    )

    result = await explain_translation(SAMPLE_TRANSLATION)

    assert isinstance(result, ExplainResponse)
    assert len(result.explanations) == 1
    assert result.explanations[0]["section"] == "What this does"


@pytest.mark.asyncio
async def test_explanation_fallback_on_exception(monkeypatch):
    """
    Service should return fallback if OpenAI raises an error.
    """

    async_mock = AsyncMock(side_effect=Exception("API failure"))

    monkeypatch.setattr(
        "ai.explanation_service.generate_explanation",
        async_mock
    )

    result = await explain_translation(SAMPLE_TRANSLATION)

    assert isinstance(result, ExplainResponse)
    assert len(result.explanations) > 0
    assert "explore" in result.explanations[0]["text"].lower()


@pytest.mark.asyncio
async def test_explanation_empty_response(monkeypatch):
    """
    Handles edge case where AI returns empty explanations.
    """

    empty_response = ExplainResponse(explanations=[])

    async_mock = AsyncMock(return_value=empty_response)

    monkeypatch.setattr(
        "ai.explanation_service.generate_explanation",
        async_mock
    )

    result = await explain_translation(SAMPLE_TRANSLATION)

    assert len(result.explanations) > 0
    assert "explore" in result.explanations[0]["text"].lower()
    