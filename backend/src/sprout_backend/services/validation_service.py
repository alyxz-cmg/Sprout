# backend/services/validation_service.py

from typing import Dict, Any


class ValidationError(Exception):
    """
    User-friendly validation error for frontend display.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# ---------- FILE VALIDATION ----------

def validate_file(file_bytes: bytes, max_size_mb: int = 5) -> None:
    """
    Validates raw uploaded file.
    """
    if not file_bytes:
        raise ValidationError("Hmm, that file looks empty. Try uploading it again!")

    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > max_size_mb:
        raise ValidationError(
            f"That file is a bit too big ({size_mb:.1f}MB). Try a smaller Scratch project!"
        )


# ---------- PROJECT STRUCTURE VALIDATION ----------

def validate_project_json(project_json: Dict[str, Any]) -> None:
    """
    Ensures the Scratch project has expected structure.
    """

    if not isinstance(project_json, dict):
        raise ValidationError("We couldn’t read your project properly. Try another file!")

    targets = project_json.get("targets")

    if not targets or not isinstance(targets, list):
        raise ValidationError(
            "This Scratch project seems to be missing its main parts. Try a different file!"
        )

    # Check at least one target has blocks
    has_blocks = False
    has_scripts = False

    for target in targets:
        blocks = target.get("blocks", {})

        if blocks:
            has_blocks = True

            # Check for top-level scripts (events)
            for block in blocks.values():
                if isinstance(block, dict) and block.get("topLevel"):
                    has_scripts = True
                    break

    if not has_blocks:
        raise ValidationError(
            "We couldn’t find any code blocks in your project yet. Try adding some blocks in Scratch!"
        )

    if not has_scripts:
        raise ValidationError(
            "Your project doesn’t have any starting blocks (like 'when green flag clicked'). Try adding one!"
        )