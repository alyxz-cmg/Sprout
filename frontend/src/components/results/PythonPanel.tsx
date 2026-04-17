import React from "react";

interface PythonPanelProps {
  code: string;
}

export function PythonPanel({ code }: PythonPanelProps) {
  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
    alert("Code copied! 🚀");
  };

  return (
    <div className="flex flex-col h-full bg-[#1e1e1e] rounded-2xl overflow-hidden shadow-inner border-2 border-slate-800">
      <div className="bg-slate-800 px-4 py-2 flex justify-between items-center">
        <span className="text-slate-300 font-mono text-sm font-bold">main.py</span>
        <button 
          onClick={copyToClipboard}
          className="text-xs bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded-full font-bold transition-colors"
        >
          Copy Code
        </button>
      </div>
      <div className="p-4 overflow-x-auto text-green-400 font-mono text-sm leading-relaxed">
        <pre>{code}</pre>
      </div>
    </div>
  );
}