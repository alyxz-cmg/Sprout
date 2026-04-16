import re
from typing import Dict, Union, Any, Tuple
from ..scratch.models import ScratchProject, ScratchBlock
from ..scratch.block_index import get_top_level_blocks, build_block_sequence
from .emitter import PythonEmitter