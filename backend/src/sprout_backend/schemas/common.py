# backend/schemas/common.py

from pydantic import BaseModel, Field
from typing import Optional, Literal


# ---------- Base Schema ----------

class StrictBaseModel(BaseModel):
    """
    Base model that forbids unexpected fields.
    Helps catch bugs early and keeps API strict.
    """
    model_config = {
        "extra": "forbid"
    }


# ---------- Warning Model ----------

class Warning(StrictBaseModel):
    """
    Structured warning used across the app.
    """
    message: str = Field(..., description="Human-readable warning message")

    # Optional classification for future use (UI badges, filtering)
    type: Literal["unsupported", "approximation", "info"] = "info"

    # Optional block reference
    block_id: Optional[str] = None


# ---------- Metadata ----------

class ProjectMetadata(StrictBaseModel):
    """
    Basic project metadata.
    """
    project_name: str