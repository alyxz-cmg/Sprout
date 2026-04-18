import React, { useState, useEffect } from "react";
import type { ExplanationSection } from "../../types/api";
import { X, Lightbulb } from "lucide-react";
import explainCat from "../../assets/explain-cat.png"; 

interface FloatingTutorProps {
  section: string;
  explanations: ExplanationSection[];
  onClose: () => void;
}

export function FloatingTutor({ section, explanations, onClose }: FloatingTutorProps) {
  const [isBubbleVisible, setIsBubbleVisible] = useState(true);

  useEffect(() => {
    setIsBubbleVisible(true);
  }, [section]);

  const isWelcome = section === "welcome";
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
    <div className="fixed bottom-6 right-6 z-50 flex items-end space-x-2">
      {isBubbleVisible && (
        <div className="relative bg-white/95 backdrop-blur-md border-4 border-blue-200/80 rounded-3xl p-5 shadow-2xl max-w-md mb-8 animate-in slide-in-from-bottom-5 fade-in duration-300">
          <button 
            onClick={() => setIsBubbleVisible(false)}
            className="absolute -top-3 -right-3 bg-red-100 hover:bg-red-200 text-red-600 rounded-full p-1 border-2 border-white shadow-sm transition-transform active:scale-95"
          >
            <X size={16} strokeWidth={3} />
          </button>

          <div className="absolute -right-3 bottom-8 w-6 h-6 bg-white border-b-4 border-r-4 border-blue-200/80 transform -rotate-45"></div>
          
          {!isWelcome && (
            <h4 className="font-extrabold text-blue-800 text-lg mb-2 flex items-center gap-2">
              <span className="text-xl">💡</span>
              {displayTitle}
            </h4>
          )}
          
          <div className="max-h-[40vh] overflow-y-auto custom-scrollbar pr-2">
            {isWelcome ? (
              <div className="text-slate-700 font-medium leading-relaxed text-sm">
                <span className="text-slate-800 font-bold text-base block mb-1">
                  Hi, I'm Sprout!
                </span>
                <span>Click on one of the </span>
                <span className="inline-flex items-center translate-y-[1px] space-x-1 px-2 py-0.5 bg-[#2d2d30] text-blue-400 border border-[#444] rounded-full text-[10px] font-bold shadow-sm cursor-default mx-0.5">
                  <Lightbulb size={10} />
                  <span>Guide</span>
                </span>
                <span> buttons and I'll explain the code!</span>
              </div>
            ) : explanation ? (
              <div className="text-slate-700 font-medium leading-relaxed whitespace-pre-wrap text-sm">
                {formatText(explanation.text)}
              </div>
            ) : (
              <p className="text-slate-500 italic text-sm">
                Hmm, I don't have specific advice for this part yet, but you're doing great!
              </p>
            )}
          </div>
        </div>
      )}

      <button 
        onClick={() => setIsBubbleVisible(!isBubbleVisible)}
        className="outline-none focus:outline-none transition-transform duration-300 hover:scale-110 active:scale-95"
      >
        <img 
          src={explainCat} 
          alt="Sprout Cat Tutor" 
          className="w-36 h-36 object-contain filter drop-shadow-xl"
        />
      </button>
    </div>
  );
}