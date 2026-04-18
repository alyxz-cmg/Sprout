import React, { useState } from "react";
import { Sprout, X, BookOpen } from "lucide-react";
import { dictionaryData } from "../../assets/dictionary/dataDictionary.ts";

export default function Header() {
  const [isDictionaryOpen, setIsDictionaryOpen] = useState(false);

  return (
    <>
      <header className="bg-green-600 text-white p-4 shadow-md flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sprout className="w-8 h-8" />
          <h1 className="text-2xl font-bold tracking-wide">Sprout</h1>
        </div>
        
        <div className="flex items-center gap-4">
          <button 
            onClick={() => setIsDictionaryOpen(true)}
            className="text-white hover:scale-110 transition-transform bg-green-700/50 hover:bg-green-700 p-2 rounded-lg"
            title="Open Block Dictionary"
          >
            <BookOpen className="w-5 h-5" />
          </button>
        </div>
      </header>

      {/* Pop-out Dictionary Modal */}
      {isDictionaryOpen && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[80vh] flex flex-col animate-in fade-in zoom-in duration-200">
            
            {/* Modal Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-100">
              <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                <BookOpen className="w-6 h-6 text-green-600" />
                Scratch to Python Dictionary
              </h2>
              <button 
                onClick={() => setIsDictionaryOpen(false)}
                className="text-red-500 hover:bg-red-50 p-1 rounded-lg transition-colors"
                title="Close"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Modal Body (Scrollable) */}
            <div className="p-6 overflow-y-auto bg-slate-50 rounded-b-2xl">
              <p className="text-slate-600 mb-6 font-medium">
                Unsure of a Python code block? Check out the Scratch mappings below!
              </p>

              {/* Dynamically Rendered Dictionary List */}
              <div className="space-y-3">
                {dictionaryData.map((item) => (
                  <div key={item.id} className="flex flex-col sm:flex-row sm:items-center gap-4 p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
                    <div className="w-1/2">
                      <span className={`${item.colorClass} px-4 py-2 rounded-full font-bold text-sm shadow-sm inline-block`}>
                        {item.scratchText}
                      </span>
                    </div>
                    <span className="hidden sm:block text-slate-300 font-bold">→</span>
                    <div className="w-1/2">
                      <code className="bg-slate-800 text-green-400 px-4 py-2 rounded-lg text-sm font-mono block overflow-x-auto">
                        {item.pythonCode}
                      </code>
                    </div>
                  </div>
                ))}
              </div>

            </div>
          </div>
        </div>
      )}
    </>
  );
}