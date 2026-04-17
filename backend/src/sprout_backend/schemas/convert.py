from pydantic import BaseModel
from typing import List, Dict, Any

class Mapping(BaseModel):
    scratch_block_id: str
    scratch_opcode: str
    python_lines: List[int]
    note: str = ""

class ConvertResponse(BaseModel):
    project_name: str
    python_code: str
    mappings: List[Mapping]
    warnings: List[str]