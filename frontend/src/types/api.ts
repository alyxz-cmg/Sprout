export interface MappingNote {
  scratch_block_id: string;
  scratch_opcode: string;
  python_lines: number[];
  note: string;
}

export interface ConvertResponse {
  project_name: string;
  python_code: string;
  mappings: MappingNote[];
  warnings: string[];
}

export interface ExplanationSection {
  section: string;
  text: string;
}

export interface ExplainResponse {
  explanations: ExplanationSection[];
}