import json
from io import BytesIO


def export_python(result: dict) -> bytes:
    """
    Returns a .py file as bytes
    """
    return result["python_code"].encode("utf-8")


def export_json(result: dict) -> bytes:
    """
    Full structured export
    """
    return json.dumps(result, indent=2).encode("utf-8")


def export_bundle(result: dict) -> bytes:
    """
    Optional: zip bundle with multiple files
    """
    import zipfile

    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("project.py", result["python_code"])
        z.writestr("report.json", json.dumps(result, indent=2))

    buffer.seek(0)
    return buffer.read()