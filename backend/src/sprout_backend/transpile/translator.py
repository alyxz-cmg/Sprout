import re
from typing import Dict, Union, Any, Tuple
from ..scratch.models import ScratchProject, ScratchBlock
from ..scratch.block_index import get_top_level_blocks, build_block_sequence
from .emitter import PythonEmitter

class ProjectTranslator:
    """
    Translates a parsed ScratchProject into a deterministic Python script,
    supporting Motion, Looks, Sound, Events, Control, Sensing, Operators, Variables, and My Blocks.
    """
    def __init__(self, project: ScratchProject):
        self.project = project
        self.emitter = PythonEmitter()
        self.blocks: Dict[str, Union[ScratchBlock, list]] = {}

    def translate(self) -> Dict[str, Any]:
        self.emitter.emit_line("import time", "meta", "import", "Imported for wait blocks.")
        self.emitter.emit_line("import random", "meta", "import", "Imported for math blocks.")
        self.emitter.lines.append("")

        for target in self.project.targets:
            self.blocks = target.blocks
            top_level_ids = get_top_level_blocks(self.blocks)
            
            if top_level_ids:
                sprite_type = "Stage" if target.isStage else "Sprite"
                self.emitter.emit_line(f"# --- {sprite_type}: {target.name} ---", "meta", "comment")
                
            for start_id in top_level_ids:
                sequence = build_block_sequence(start_id, self.blocks)
                self._translate_sequence(sequence)
                self.emitter.lines.append("") 
                
        return {
            "python_code": self.emitter.get_code(),
            "mappings": self.emitter.mappings,
            "warnings": self.emitter.warnings
        }

    def _translate_sequence(self, sequence: list[str]):
        for block_id in sequence:
            block = self.blocks.get(block_id)
            if isinstance(block, ScratchBlock):
                self._translate_block(block_id, block)

    def _resolve_input(self, block: ScratchBlock, input_name: str, default: str = "0") -> str:
        """
        Recursively resolves an input. It might be a simple number/string,
        or it might be a nested block (like an Operator or Variable).
        """
        if input_name not in block.inputs:
            return default
            
        input_data = block.inputs[input_name]
        if not isinstance(input_data, list) or len(input_data) < 2:
            return default
            
        val_data = input_data[1]
        
        # If it's a string, it's likely a reference to another block (a reporter)
        if isinstance(val_data, str):
            return self._evaluate_reporter(val_data)
            
        # If it's a list, it's a literal value (e.g., [4, "10"], [10, "hello"])
        if isinstance(val_data, list) and len(val_data) > 1:
            val = str(val_data[1])
            # Quote strings, leave numbers
            if not val.replace('.', '', 1).isdigit() and not val.startswith(('sprite.', 'var_')):
                return f'"{val}"'
            return val
            
        return default

    def _get_field(self, block: ScratchBlock, field_name: str, default: str = "") -> str:
        """Extracts field selections (e.g., dropdown menus)."""
        if field_name in block.fields:
            return str(block.fields[field_name][0])
        return default

    def _sanitize_name(self, name: str) -> str:
        """Sanitizes Scratch variable or custom block names to valid Python identifiers."""
        clean = re.sub(r'\W|^(?=\d)', '_', name)
        return clean.lower()