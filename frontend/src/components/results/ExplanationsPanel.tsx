import React from "react";
import type { ExplanationSection } from "../../types/api";

interface ExplanationsPanelProps {
  explanations: ExplanationSection[];
}

export function ExplanationsPanel({ explanations }: ExplanationsPanelProps) {
  
  // Helper function to turn backticks into bold, stylized code badges
  const formatText = (text: string) => {
    const parts = text.split(/`([^`]+)`/g);
    
    return parts.map((part, index) => {

      if (index % 2 === 1) {
        return (
          <span 
            key={index} 
            className="bg-blue-100 text-blue-900 font-bold font-mono px-2 py-0.5 rounded-md text-sm mx-0.5 border border-blue-200"
          >
            {part}
          </span>
        );
      }

      return part;
    });
  };

  return (
    <div className="bg-blue-50 border-2 border-blue-200 rounded-2xl p-6 h-full shadow-sm">
      <div className="flex items-center gap-3 mb-6">
        <span className="text-3xl">🦉</span>
        <h3 className="font-extrabold text-blue-900 text-2xl">Your Guide</h3>
      </div>
      
      <div className="space-y-6">
        {explanations.map((exp, idx) => (
          <div key={idx} className="bg-white p-4 rounded-xl shadow-sm border border-blue-100">
            <h4 className="font-bold text-blue-800 text-lg mb-2">{exp.section}</h4>
            <p className="text-slate-700 font-medium leading-relaxed whitespace-pre-wrap">
              {formatText(exp.text)}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}