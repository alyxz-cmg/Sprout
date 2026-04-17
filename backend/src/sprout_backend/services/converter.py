# backend/services/converter.py

from ..core.loader import load_sb3
from ..core.parser import parse_project
from ..core.translator import translate_project
from .validation_service import validate_file, validate_project_json


def convert_sb3(file_bytes: bytes) -> dict:
    """
    Full deterministic conversion pipeline.
    """

    # Validate raw file
    validate_file(file_bytes)

    # Load
    project_json = load_sb3(file_bytes)

    # Validate structure
    validate_project_json(project_json)

    # Parse + translate
    ir = parse_project(project_json)
    translation = translate_project(ir)

    return {
        "project_name": ir.name,
        "warnings": translation["warnings"],
        "python_code": translation["python_code"],
        "mappings": translation["mappings"],
    }