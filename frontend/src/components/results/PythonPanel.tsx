import React, { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Copy, Check, EyeOff, Eye, Lightbulb } from "lucide-react";

interface PythonPanelProps {
  code: string;
  activeSection?: string | null;
  onHintClick?: (section: string) => void;
}

export function PythonPanel({ code, activeSection, onHintClick }: PythonPanelProps) {
  const [copied, setCopied] = useState(false);
  const [showHints, setShowHints] = useState(true);

  const copyToClipboard = () => {
    const cleanCode = code.replace(/### SECTION:.*\n?/g, '');
    navigator.clipboard.writeText(cleanCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // --- CHUNKING LOGIC ---
  const lines = code.split('\n');
  const chunks: any[] = [];
  let currentChunkCode: string[] = [];
  let currentStartLine = 1;
  let activeSectionForChunk: string | null = null;

  lines.forEach((line, index) => {
    const match = line.match(/### SECTION:\s*(.*)/);
    if (match) {
      if (currentChunkCode.length > 0) {
        chunks.push({
          type: 'code',
          code: currentChunkCode.join('\n'),
          startLine: currentStartLine,
          associatedSection: activeSectionForChunk
        });
      }

      const fullName = match[1].trim();
      
      const displayName = fullName.replace(/\s*\(ID:\s*\d+\)/g, "");

      chunks.push({ 
        type: 'section', 
        name: fullName,
        label: displayName
      });
      
      currentChunkCode = [];
      currentStartLine = index + 2; 
      activeSectionForChunk = fullName;
    } else {
      currentChunkCode.push(line);
    }
  });

  if (currentChunkCode.length > 0) {
    chunks.push({ type: 'code', code: currentChunkCode.join('\n'), startLine: currentStartLine, associatedSection: activeSectionForChunk });
  }

  return (
    <div className="flex flex-col h-full bg-[#1e1e1e]/90 backdrop-blur-md rounded-xl overflow-hidden shadow-2xl border border-white/20">
      <div className="bg-[#252526]/80 px-4 py-1 flex justify-between items-center border-b border-white/10">
        <div className="flex items-center space-x-2 bg-[#1e1e1e]/80 px-4 py-2 border-t border-t-[#007acc] rounded-t-sm">
          <span className="text-[#cccccc] font-mono text-xs">main.py</span>
        </div>
        
        <div className="flex items-center space-x-2">
          <button 
            onClick={() => setShowHints(!showHints)}
            className="flex items-center space-x-1.5 px-2 py-1.5 hover:bg-[#37373d] text-[#cccccc] text-xs font-medium rounded-md transition-all active:scale-95"
          >
            {showHints ? <EyeOff size={14} /> : <Eye size={14} />}
            <span>{showHints ? "Hide Guides" : "Show Guides"}</span>
          </button>

          <div className="w-px h-4 bg-[#444] mx-1"></div>

          <button 
            onClick={copyToClipboard}
            className="flex items-center space-x-1.5 px-2 py-1.5 hover:bg-[#37373d] text-[#cccccc] text-xs font-medium rounded-md transition-all active:scale-95"
            title="Copy Code"
          >
            {copied ? <Check size={14} className="text-green-500" /> : <Copy size={14} />}
            <span>Copy</span>
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-auto bg-transparent text-sm custom-scrollbar py-4">
        {chunks.map((chunk, idx) => {
          if (chunk.type === 'section') {
            if (!showHints) return null;

            const isSelected = activeSection === chunk.name;

            return (
              <div key={idx} className="px-4 py-2 my-1 flex items-center">
                 <div className="w-10"></div>
                 <button
                   onClick={() => onHintClick && onHintClick(chunk.name)}
                   className={`flex items-center space-x-2 px-3 py-1.5 rounded-full text-xs font-bold transition-all transform hover:scale-105 shadow-md ${
                     isSelected 
                       ? "bg-green-500 text-white ring-2 ring-green-300 ring-offset-2 ring-offset-[#1e1e1e]" 
                       : "bg-[#2d2d30] text-blue-400 hover:bg-[#3e3e42] border border-[#444]"
                   }`}
                 >
                   <Lightbulb size={14} className={isSelected ? "animate-pulse text-yellow-300" : ""} />
                   <span>Guide: {chunk.label}</span>
                   <span className="text-[10px] opacity-70 ml-1">➔</span>
                 </button>
              </div>
            );
          }

          const isHighlighted = showHints && activeSection === chunk.associatedSection;
          
          return (
            <div 
              key={idx} 
              className={`transition-colors duration-500 ${isHighlighted ? "bg-[#062f4a]/40 border-l-[3px] border-blue-500" : "border-l-[3px] border-transparent"}`}
            >
              <SyntaxHighlighter
                language="python"
                style={vscDarkPlus}
                startingLineNumber={chunk.startLine}
                customStyle={{
                  margin: 0,
                  padding: 0,
                  backgroundColor: 'transparent',
                  fontSize: '0.875rem',
                  lineHeight: '1.5',
                  textAlign: 'left',
                }}
                showLineNumbers={true}
                lineNumberStyle={{ 
                  minWidth: '3em', 
                  paddingRight: '1em', 
                  color: isHighlighted ? '#a0c7e8' : '#858585', 
                  textAlign: 'right',
                  userSelect: 'none'
                 }}
              >
                {chunk.code || " "} 
              </SyntaxHighlighter>
            </div>
          );
        })}
      </div>
    </div>
  );
}