import React from "react";
import type { ExplanationSection } from "../../types/api";
import { X } from "lucide-react";
import explainCat from "../../assets/explain-cat.png"; 

interface FloatingTutorProps {
  section: string;
  explanations: ExplanationSection[];
  onClose: () => void;
}

export function FloatingTutor({ section, explanations, onClose }: FloatingTutorProps) {
  // --- ID STRIPPING LOGIC ---
  const displayTitle = section.replace(/\s*\(ID:\s*\d+\)/g, "");

  const explanation = explanations.find(
    (e) => e.section.trim().toLowerCase() === section.trim().toLowerCase()
  );

  const formatText = (text: string) => {
    const parts = text.split(/`([^`]+)`/g);
    return parts.map((part, index) => {
      if (index % 2 === 1) {
        return (
          <span key={index} className="bg-blue-100/60 text-blue-900 font-bold font-mono px-1.5 py-0.5 rounded text-[13px] mx-0.5 border border-blue-200">
            {part}
          </span>
        );
      }
      return part;
    });
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex items-end space-x-2 animate-in slide-in-from-bottom-10 fade-in duration-500">
      
      {/* Speech Bubble */}
      <div className="relative bg-white border-4 border-blue-200 rounded-3xl p-5 shadow-2xl max-w-md mb-8">
        {/* Close Button */}
        <button 
          onClick={onClose}
          className="absolute -top-3 -right-3 bg-red-100 hover:bg-red-200 text-red-600 rounded-full p-1 border-2 border-white shadow-sm transition-transform active:scale-95"
        >
          <X size={16} strokeWidth={3} />
        </button>

        {/* CSS Triangle Arrow pointing to the cat */}
        <div className="absolute -right-3 bottom-8 w-6 h-6 bg-white border-b-4 border-r-4 border-blue-200 transform -rotate-45"></div>
        
        <h4 className="font-extrabold text-blue-800 text-lg mb-2 flex items-center gap-2">
          <span className="text-xl">💡</span>
          {displayTitle}
        </h4>
        
        <div className="max-h-[40vh] overflow-y-auto custom-scrollbar pr-2">
          {explanation ? (
            <div className="text-slate-700 font-medium leading-relaxed whitespace-pre-wrap text-sm">
              {formatText(explanation.text)}
            </div>
          ) : (
            <div className="space-y-2">
              <p className="text-slate-500 italic text-sm">
                Hmm, I don't have specific advice for this part yet, but you're doing great! Keep looking at the code!
              </p>
              {/* Optional: Debug info for developers - remove in production */}
              {/* <p className="text-[10px] text-slate-300">Searching for: {section}</p> */}
            </div>
          )}
        </div>
      </div>

      {/* Interactive Cat */}
      <img 
        src={explainCat} 
        alt="Sprout Cat Tutor" 
        className="w-36 h-36 object-contain hover:scale-105 transition-transform duration-300 origin-bottom filter drop-shadow-xl"
      />
    </div>
  );
}