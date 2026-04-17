from ..core.loader import load_sb3
from ..core.parser import parse_project
from ..core.translator import translate_project


def convert_sb3(file_bytes: bytes) -> dict:
    """
    Full deterministic conversion pipeline.
    No AI used here.
    """
    project_json = load_sb3(file_bytes)
    ir = parse_project(project_json)
    translation = translate_project(ir)

    return {
        "project_name": ir.name,
        "warnings": translation["warnings"],
        "python_code": translation["python_code"],
        "mappings": translation["mappings"],
    }