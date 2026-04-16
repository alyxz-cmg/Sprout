from typing import List, Dict, Any

class PythonEmitter:
    """
    A helper class to construct Python code string line-by-line while tracking 
    the mapping between generated lines and the original Scratch block IDs.
    """
    def __init__(self):
        self.lines: List[str] = []
        self.mappings: List[Dict[str, Any]] = []
        self.current_indent: int = 0
        self.warnings: List[str] = []

    def indent(self):
        self.current_indent += 1

    def dedent(self):
        self.current_indent = max(0, self.current_indent - 1)

    def emit_line(self, code: str, block_id: str, opcode: str, note: str = ""):
        """
        Appends a line of Python code and records its source block mapping.
        """
        indentation = "    " * self.current_indent
        full_line = f"{indentation}{code}"
        self.lines.append(full_line)
        
        # Line numbers are 1-indexed
        line_number = len(self.lines) 
        
        self.mappings.append({
            "scratch_block_id": block_id,
            "scratch_opcode": opcode,
            "python_lines": [line_number],
            "note": note
        })

    def add_warning(self, message: str):
        """Records a warning for unsupported or approximated blocks."""
        if message not in self.warnings:
            self.warnings.append(message)

    def get_code(self) -> str:
        return "\n".join(self.lines)