from fastapi import APIRouter, UploadFile, File, HTTPException
from ...scratch.loader import load_sb3_from_bytes
from ...transpile.translator import ProjectTranslator
from ...schemas.convert import ConvertResponse
from ...core.exceptions import SproutBaseException

router = APIRouter()

@router.post("/convert", response_model=ConvertResponse)
async def convert_sb3(file: UploadFile = File(...)):
    """
    Accepts an uploaded .sb3 file, unzips it, parses the Scratch AST,
    and returns deterministic Python code along with mapping data.
    """
    if not file.filename.endswith('.sb3'):
        raise HTTPException(status_code=400, detail="File must be an .sb3 file.")

    try:
        # Read the file into memory
        file_bytes = await file.read()

        project = load_sb3_from_bytes(file_bytes)

        translator = ProjectTranslator(project)
        result = translator.translate()

        raw_warnings = result.get("warnings", [])
        formatted_warnings = []
        for w in raw_warnings:
            if isinstance(w, dict):
                msg = w.get("message", "Unknown error")
                bid = w.get("block_id", "unknown")
                formatted_warnings.append(f"{msg} (Block: {bid})")
            else:
                formatted_warnings.append(str(w))

        # Default project name fallback
        project_name = file.filename.replace('.sb3', '')

        return ConvertResponse(
            project_name=project_name,
            python_code=result["python_code"],
            mappings=result["mappings"],
            warnings=formatted_warnings
        )
    
    except SproutBaseException as e:
        # Catch our domain-specific exceptions and return clean 400s
        raise HTTPException(status_code=400, detail=e.message)
    
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}") 
        raise HTTPException(status_code=500, detail="Something went wrong while processing your project.")