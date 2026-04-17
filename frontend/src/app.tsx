import React, { useState } from "react";
import { convertProject } from "./api/convert";
import { explainTranslation } from "./api/explain";
import type { ConvertResponse, ExplainResponse } from "./types/api";

type AppState = "idle" | "converting" | "explaining" | "success" | "error";

export default function App() {
  const [appState, setAppState] = useState<AppState>("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [convertData, setConvertData] = useState<ConvertResponse | null>(null);
  const [explainData, setExplainData] = useState<ExplainResponse | null>(null);

  const handleFileUpload = async (file: File) => {
    try {
      // 1. Reset state and start conversion
      setAppState("converting");
      setErrorMessage(null);
      
      const converted = await convertProject(file);
      setConvertData(converted);

      // 2. Start explanation phase using the successful conversion data
      setAppState("explaining");
      
      const explained = await explainTranslation(converted);
      setExplainData(explained);

      // 3. Mark as completely successful
      setAppState("success");

    } catch (error: any) {
      setAppState("error");
      setErrorMessage(error.message || "Something went wrong while growing your code.");
    }
  };

  const resetApp = () => {
    setAppState("idle");
    setConvertData(null);
    setExplainData(null);
    setErrorMessage(null);
  };

  return (
    <div className="min-h-screen bg-green-50 text-slate-800 p-8 font-sans">
      <header className="max-w-4xl mx-auto mb-8 text-center">
        <h1 className="text-4xl font-extrabold text-green-600 mb-2">🌱 Sprout</h1>
        <p className="text-lg text-slate-600">Grow your Scratch blocks into Python code!</p>
      </header>

      <main className="max-w-4xl mx-auto bg-white rounded-2xl shadow-sm p-6 border border-green-100">
        
        {/* Placeholder for Phase 5 UI Components */}
        {appState === "idle" && (
          <div className="text-center p-12 border-2 border-dashed border-green-200 rounded-xl bg-green-50/50">
            <h2 className="text-xl font-bold mb-4">Upload your .sb3 file</h2>
            <input 
              type="file" 
              accept=".sb3" 
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleFileUpload(file);
              }}
              className="block w-full max-w-sm mx-auto text-sm text-slate-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-green-100 file:text-green-700
                hover:file:bg-green-200 cursor-pointer"
            />
          </div>
        )}

        {(appState === "converting" || appState === "explaining") && (
          <div className="text-center p-12 animate-pulse">
            <div className="text-5xl mb-4">⚙️</div>
            <h2 className="text-xl font-bold text-slate-700">
              {appState === "converting" ? "Translating your blocks..." : "Writing your explanations..."}
            </h2>
          </div>
        )}

        {appState === "error" && (
          <div className="bg-red-50 text-red-700 p-6 rounded-xl text-center border border-red-200">
            <h2 className="text-xl font-bold mb-2">Oops! We hit a snag.</h2>
            <p className="mb-4">{errorMessage}</p>
            <button 
              onClick={resetApp}
              className="bg-red-100 hover:bg-red-200 text-red-800 font-bold py-2 px-6 rounded-full transition-colors"
            >
              Try Again
            </button>
          </div>
        )}

        {appState === "success" && convertData && explainData && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-green-700">Project: {convertData.project_name}</h2>
              <button 
                onClick={resetApp}
                className="text-sm font-semibold text-slate-500 hover:text-slate-800"
              >
                Start Over
              </button>
            </div>
            {/* These sections will be replaced by actual components in Phase 5 */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-900 text-green-400 p-4 rounded-xl font-mono text-sm overflow-x-auto">
                <pre>{convertData.python_code}</pre>
              </div>
              <div className="bg-blue-50 border border-blue-100 p-4 rounded-xl space-y-4">
                <h3 className="font-bold text-blue-800 text-lg">Your Guide</h3>
                {explainData.explanations.map((exp, idx) => (
                  <div key={idx}>
                    <h4 className="font-bold text-slate-800">{exp.section}</h4>
                    <p className="text-slate-600 text-sm leading-relaxed">{exp.text}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}