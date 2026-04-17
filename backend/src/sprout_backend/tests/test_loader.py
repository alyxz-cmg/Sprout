import json
import zipfile
from io import BytesIO
import pytest

from scratch.loader import load_sb3, InvalidScratchFile


# --- Helper to create in-memory .sb3 files ---

def make_sb3(project_data: dict) -> bytes:
    """
    Creates a valid in-memory .sb3 file with project.json
    """
    buffer = BytesIO()

    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("project.json", json.dumps(project_data))

    buffer.seek(0)
    return buffer.read()


# --- TESTS ---


def test_load_valid_sb3():
    """
    Should successfully load a valid .sb3 file.
    """
    project_data = {
        "targets": [],
        "meta": {"semver": "3.0.0"}
    }

    sb3_bytes = make_sb3(project_data)

    result = load_sb3(sb3_bytes)

    assert result == project_data


def test_missing_project_json():
    """
    Should raise error if project.json is missing.
    """
    buffer = BytesIO()

    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("not_project.json", "{}")

    buffer.seek(0)

    with pytest.raises(InvalidScratchFile) as exc:
        load_sb3(buffer.read())

    assert "project.json" in str(exc.value)


def test_invalid_zip_file():
    """
    Should raise error for invalid zip files.
    """
    bad_bytes = b"this is not a zip file"

    with pytest.raises(InvalidScratchFile):
        load_sb3(bad_bytes)