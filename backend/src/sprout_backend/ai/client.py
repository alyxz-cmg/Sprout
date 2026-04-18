import os
import json
from openai import AsyncOpenAI
from pydantic import ValidationError
from dotenv import load_dotenv
from .prompts import SYSTEM_PROMPT
from ..schemas.explain import ExplainResponse


load_dotenv()
# Initialize the async client. It automatically picks up OPENAI_API_KEY from the environment.
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async def generate_explanation(translation_data: dict) -> ExplainResponse:
    """
    Sends the deterministic translation payload to OpenAI and requests
    a structured JSON response explaining the code to a child.
    """
    # Convert the payload to a formatted string for the prompt
    payload_str = json.dumps(translation_data, indent=2)
    user_prompt = f"Here is the translated Scratch project data:\n{payload_str}\n\nPlease explain this translation."

    try:
        response = await client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06", # Using a model that supports strict structured parsing
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format=ExplainResponse,
            temperature=0.4 # Keep it relatively deterministic and focused
        )
        return response.choices[0].message.parsed
    
    except Exception as e:
        # Fallback if the AI fails, so the app doesn't crash entirely for the user
        return ExplainResponse(
            explanations=[
                {
                    "section": "Oops!",
                    "text": "I had a little trouble generating an explanation right now, but your Python code is ready above! Keep exploring."
                }
            ]
        )