import os
import json
from openai import AsyncOpenAI
from pydantic import ValidationError
from dotenv import load_dotenv
from .prompts import SYSTEM_PROMPT
from ..schemas.explain import ExplainResponse

load_dotenv()

# Initialize the async client. It automatically picks up GEMINI_API_KEY from the environment.
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async def generate_explanation(translation_data: dict) -> ExplainResponse:
    """
    Sends the deterministic translation payload to Gemini and requests
    a structured JSON response explaining the code to a child.
    """
    # Convert the payload to a formatted string for the prompt
    payload_str = json.dumps(translation_data, indent=2)
    
    # Explicitly remind the model to output raw JSON so it plays nicely
    user_prompt = f"Here is the translated Scratch project data:\n{payload_str}\n\nPlease explain this translation. Return ONLY valid JSON."

    try:
        response = await client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4 # Keep it relatively deterministic and focused
        )
        
        content = response.choices[0].message.content.strip()
        
        # Strip out markdown backticks if the AI still adds them
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        # Parse the raw string into a Python dictionary
        parsed_data = json.loads(content)
        
        return ExplainResponse(**parsed_data)
    
    except Exception as e:
        print(f"🔥 AI GENERATION ERROR: {e}")
        
        # Fallback if the AI fails, so the app doesn't crash entirely for the user
        return ExplainResponse(
            explanations=[
                {
                    "section": "Oops!",
                    "text": "I had a little trouble generating an explanation right now, but your Python code is ready above! Keep exploring."
                }
            ]
        )