import os
import json
import re
from openai import AsyncOpenAI
from pydantic import ValidationError
from dotenv import load_dotenv
from .prompts import SYSTEM_PROMPT
from ..schemas.explain import ExplainResponse

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async def generate_explanation(translation_data: dict) -> ExplainResponse:
    payload_str = json.dumps(translation_data, indent=2)
    user_prompt = f"Here is the translated Scratch project data:\n{payload_str}\n\nPlease explain this translation. Return ONLY valid JSON."

    try:
        response = await client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4
        )
        
        content = response.choices[0].message.content.strip()
        
        # Helper to clean and validate the dictionary
        def repair_and_validate(data):
            # Fix singular/plural top-level key
            if "explanation" in data and "explanations" not in data:
                data["explanations"] = data.pop("explanation")
            
            # Fix keys inside the list
            if isinstance(data.get("explanations"), list):
                for item in data["explanations"]:
                    if isinstance(item, dict):
                        if "title" in item and "section" not in item:
                            item["section"] = item.pop("title")
                        
                        if "text" in item and isinstance(item["text"], list):
                            item["text"] = "\n".join(f"• {bullet}" for bullet in item["text"])
            
            # Coerce string explanations into the required list format
            if isinstance(data.get("explanations"), str):
                data["explanations"] = [{"section": "Overview", "text": data["explanations"]}]
            
            return ExplainResponse(**data)

        # First Attempt: Try parsing the whole content
        try:
            # Strip markdown backticks
            clean_content = re.sub(r'^```json\s*|```$', '', content, flags=re.MULTILINE).strip()
            return repair_and_validate(json.loads(clean_content))
        except (json.JSONDecodeError, ValidationError):
            # Second Attempt: Use RegEx to find the first JSON object {} in the string
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    return repair_and_validate(json.loads(json_match.group()))
                except:
                    pass

        # Final Emergency Fallback: If it's just raw text, wrap it nicely
        return ExplainResponse(
            explanations=[{"section": "How it works", "text": content}]
        )
    
    except Exception as e:
        print(f"🔥 CRITICAL ERROR: {e}")
        return ExplainResponse(
            explanations=[{"section": "Oops!", "text": "Something went wrong. But look at that code!"}]
        )