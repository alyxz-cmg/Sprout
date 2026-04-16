import zipfile
import json
import io
from pydantic import ValidationError
from .models import ScratchProject
from ..core.exceptions import InvalidSB3Error, ProjectJSONNotFoundError, ParsingError

def load_sb3_from_bytes(file_bytes: bytes) -> ScratchProject:
    """
    Reads an .sb3 file (ZIP format) from memory, extracts project.json,
    and parses it into strongly-typed Pydantic models.
    
    Args:
        file_bytes (bytes): The raw bytes of the uploaded .sb3 file.
        
    Returns:
        ScratchProject: The validated representation of the Scratch project.
        
    Raises:
        InvalidSB3Error: If the bytes are not a valid ZIP archive.
        ProjectJSONNotFoundError: If project.json is missing.
        ParsingError: If the JSON is invalid or fails schema validation.
    """
    try:
        archive = zipfile.ZipFile(io.BytesIO(file_bytes))
    except zipfile.BadZipFile:
        raise InvalidSB3Error(
            "The uploaded file doesn't look like a valid Scratch project. "
            "Make sure it's an .sb3 file!"
        )

    if "project.json" not in archive.namelist():
        raise ProjectJSONNotFoundError(
            "We couldn't find the 'project.json' inside your .sb3 file. "
            "The file might be corrupted."
        )

    try:
        with archive.open("project.json") as f:
            project_data = json.load(f)
    except json.JSONDecodeError:
        raise ParsingError("The project data is unreadable (invalid JSON).")

    try:
        # Hydrate the Pydantic models
        project = ScratchProject.model_validate(project_data)
        return project
    except ValidationError as e:
        # Log the exact error for debugging, but return a clean error to the user
        raise ParsingError("We had trouble understanding the structure of this Scratch project.") from e