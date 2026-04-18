import { ArrowRightLeft } from "lucide-react";
import type { MappingNote } from "../../types/api";

interface MappingPanelProps {
  mappings: MappingNote[];
}

export default function MappingPanel({ mappings }: MappingPanelProps) {
  if (!mappings || mappings.length === 0) return null;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden flex flex-col h-full">
      <div className="bg-indigo-50 p-4 border-b border-indigo-100 flex items-center gap-2">
        <ArrowRightLeft className="text-indigo-600 w-5 h-5" />
        <h3 className="font-semibold text-indigo-900">Block Mapping</h3>
      </div>
      <div className="p-4 space-y-4 overflow-y-auto flex-grow">
        {mappings.map((map, index) => (
          <div key={index} className="grid grid-cols-1 md:grid-cols-2 gap-2 pb-4 border-b border-gray-100 last:border-0 last:pb-0">
            <div className="bg-orange-50 p-3 rounded-lg text-sm font-mono text-orange-800 flex items-center">
              {map.scratch_opcode}
            </div>
            <div className="bg-gray-800 p-3 rounded-lg text-sm font-mono text-green-400 whitespace-pre-wrap">
              {/* If API puts the Python code in 'note', we display it here */}
              {map.note}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}