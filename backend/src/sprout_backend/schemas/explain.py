from pydantic import BaseModel
from typing import List
from .convert import ConvertResponse

class ExplanationSection(BaseModel):
    section: str
    text: str

class ExplainRequest(BaseModel):
    translation_data: ConvertResponse
    
class ExplainResponse(BaseModel):
    explanations: List[ExplanationSection]