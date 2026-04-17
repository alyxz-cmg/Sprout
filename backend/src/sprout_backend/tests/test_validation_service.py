import pytest

from services.validation_service import (
    validate_file,
    validate_project_json,
    ValidationError,
)


# --- FILE TESTS ---


def test_empty_file():
    with pytest.raises(ValidationError):
        validate_file(b"")


def test_file_too_large():
    big_file = b"x" * (6 * 1024 * 1024)  # 6MB

    with pytest.raises(ValidationError):
        validate_file(big_file)


# --- PROJECT TESTS ---


def test_valid_project():
    project = {
        "targets": [
            {
                "blocks": {
                    "b1": {"topLevel": True}
                }
            }
        ]
    }

    validate_project_json(project)  # should not raise


def test_missing_targets():
    with pytest.raises(ValidationError):
        validate_project_json({})


def test_no_blocks():
    project = {
        "targets": [
            {"blocks": {}}
        ]
    }

    with pytest.raises(ValidationError):
        validate_project_json(project)


def test_no_top_level_scripts():
    project = {
        "targets": [
            {
                "blocks": {
                    "b1": {"topLevel": False}
                }
            }
        ]
    }

    with pytest.raises(ValidationError):
        validate_project_json(project)