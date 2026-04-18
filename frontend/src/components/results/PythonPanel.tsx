import React, { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Copy, Check } from "lucide-react";

interface PythonPanelProps {
  code: string;
}

export function PythonPanel({ code }: PythonPanelProps) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col h-full bg-[#1e1e1e] rounded-xl overflow-hidden shadow-2xl border border-[#333333]">
      {/* Tab Bar Style */}
      <div className="bg-[#252526] px-4 py-1 flex justify-between items-center border-b border-[#1e1e1e]">
        <div className="flex items-center space-x-2 bg-[#1e1e1e] px-4 py-2 border-t border-t-[#007acc] rounded-t-sm">
          <span className="text-[#cccccc] font-mono text-xs">main.py</span>
        </div>
        
        <button 
          onClick={copyToClipboard}
          className="p-1.5 hover:bg-[#37373d] text-[#cccccc] rounded-md transition-all active:scale-95"
          title="Copy Code"
        >
          {copied ? <Check size={16} className="text-green-500" /> : <Copy size={16} />}
        </button>
      </div>

      {/* Code Area */}
      <div className="flex-1 overflow-auto bg-[#1e1e1e] text-sm custom-scrollbar">
        <SyntaxHighlighter
          language="python"
          style={vscDarkPlus}
          customStyle={{
            margin: 0,
            padding: '1.5rem',
            backgroundColor: 'transparent',
            fontSize: '0.875rem',
            lineHeight: '1.5',
          }}
          showLineNumbers={true}
          lineNumberStyle={{ minWidth: '2.5em', paddingRight: '1em', color: '#858585', textAlign: 'right' }}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}