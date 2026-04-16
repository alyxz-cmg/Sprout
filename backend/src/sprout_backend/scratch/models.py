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

class ScratchTarget(BaseModel):
    """
    Represents a Sprite or the Stage in a Scratch project.
    Contains the blocks, variables, and lists specific to that target.
    """
    model_config = ConfigDict(extra="ignore")
    
    isStage: bool
    name: str
    # Variables and lists in Scratch are represented as [name, value] or [name, value, isCloud]
    variables: Dict[str, list] = Field(default_factory=dict)
    lists: Dict[str, list] = Field(default_factory=dict)
    broadcasts: Dict[str, str] = Field(default_factory=dict)
    
    # In some rare cases, Scratch represents top-level variable reporters as lists.
    # We use a Union to safely catch those without crashing the parser.
    blocks: Dict[str, Union[ScratchBlock, list]] = Field(default_factory=dict)

class ScratchProject(BaseModel):
    """
    The root schema for a Scratch 3.0 project.json file.
    """
    model_config = ConfigDict(extra="ignore")
    
    targets: List[ScratchTarget]
    meta: Dict[str, Any] = Field(default_factory=dict)