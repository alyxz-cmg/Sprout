import React, { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

interface WarningBannerProps {
  warnings: string[];
}

export function WarningBanner({ warnings }: WarningBannerProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!warnings || warnings.length === 0) return null;

  return (
    <div className="bg-amber-50 border border-amber-200 rounded-xl overflow-hidden transition-all duration-300 shadow-sm">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-4 flex items-center justify-between bg-amber-50/50 hover:bg-amber-100/50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="text-xl">🚧</span>
          <div className="text-left">
            <h3 className="font-bold text-amber-900">Translation Notes</h3>
            <p className="text-amber-700/80 text-sm font-medium">
              {warnings.length} {warnings.length === 1 ? "detail" : "details"} to review
            </p>
          </div>
        </div>
        <div className="bg-amber-200/50 p-1.5 rounded-md">
          {isExpanded ? (
            <ChevronUp className="text-amber-700 w-5 h-5" />
          ) : (
            <ChevronDown className="text-amber-700 w-5 h-5" />
          )}
        </div>
      </button>

      {isExpanded && (
        <div className="p-4 pt-0 border-t border-amber-200/50 bg-amber-50/30 animate-in slide-in-from-top-2 duration-200">
          <p className="text-amber-800 mb-3 font-medium text-sm mt-4">
            Python and Scratch are a little different! We couldn't translate everything perfectly, but we did our best. Here is what we skipped or guessed:
          </p>
          <ul className="list-disc list-inside text-sm text-amber-700 space-y-1.5 font-medium bg-amber-100/40 p-4 rounded-lg border border-amber-200/50">
            {warnings.map((warning, idx) => (
              <li key={idx} className="leading-relaxed">{warning}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}