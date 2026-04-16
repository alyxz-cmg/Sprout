import zipfile
import json
import io
from pydantic import ValidationError
from .models import ScratchProject
from ..core.exceptions import InvalidSB3Error, ProjectJSONNotFoundError, ParsingError