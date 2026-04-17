from fastapi import APIRouter
from ...schemas.explain import ExplainRequest, ExplainResponse
from ...ai.client import generate_explanation
router = APIRouter()
@router.post("/explain", response_model=ExplainResponse)
async def explain_translation(request: ExplainRequest):
    """
    Takes the output from the /convert endpoint and returns
    a kid-friendly explanation of the Python code using OpenAI.
    """
    # Convert Pydantic model to dict for the AI client
    translation_dict = request.translation_data.model_dump()
    explanation = await generate_explanation(translation_dict)
    return explanation
