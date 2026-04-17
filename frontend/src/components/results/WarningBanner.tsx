import React from "react";

interface WarningBannerProps {
  warnings: string[];
}

export function WarningBanner({ warnings }: WarningBannerProps) {
  if (!warnings || warnings.length === 0) return null;

  return (
    <div className="bg-orange-50 border-2 border-orange-200 rounded-2xl p-4 mb-6 flex items-start gap-3">
      <div className="text-2xl mt-1">🚧</div>
      <div>
        <h3 className="font-bold text-orange-800 text-lg">Under Construction!</h3>
        <p className="text-orange-700 mb-2 font-medium text-sm">
          Python and Scratch are a little different! We couldn't translate everything perfectly, but we did our best. Here is what we skipped or guessed:
        </p>
        <ul className="list-disc list-inside text-sm text-orange-600 space-y-1 font-medium">
          {warnings.map((warning, idx) => (
            <li key={idx}>{warning}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}