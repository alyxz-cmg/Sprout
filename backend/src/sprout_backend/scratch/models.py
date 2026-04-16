from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Any, List, Optional, Union

class ScratchBlock(BaseModel):
    """
    Represents a single block in the Scratch AST.
    Scratch stores blocks as a flat dictionary, linked via 'next' and 'parent' IDs.
    """
    model_config = ConfigDict(extra="ignore")
    
    opcode: str
    next: Optional[str] = None
    parent: Optional[str] = None
    inputs: Dict[str, Any] = Field(default_factory=dict)
    fields: Dict[str, Any] = Field(default_factory=dict)
    shadow: bool = False
    topLevel: bool = False