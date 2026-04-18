import React, { useState } from "react";
import { convertProject } from "./api/convert";
import { explainTranslation } from "./api/explain";
import type { ConvertResponse, ExplainResponse } from "./types/api";

// Layout & UI Components
import PageShell from "./components/layout/PageShell";
import UploadCard from "./components/UploadCard";
import { PythonPanel } from "./components/results/PythonPanel";
import { ExplanationsPanel } from "./components/results/ExplanationsPanel";
import { WarningBanner } from "./components/results/WarningBanner";
import MappingPanel from "./components/results/MappingPanel";

type AppState = "idle" | "converting" | "explaining" | "success" | "error";

export default function App() {
  const [appState, setAppState] = useState<AppState>("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [convertData, setConvertData] = useState<ConvertResponse | null>(null);
  const [explainData, setExplainData] = useState<ExplainResponse | null>(null);
  const [activeSection, setActiveSection] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    try {
      setAppState("converting");
      setErrorMessage(null);
      
      const converted = await convertProject(file);
      setConvertData(converted);

      setAppState("explaining");
      
      const explained = await explainTranslation(converted);
      setExplainData(explained);

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
    setActiveSection(null);
  };

  return (
    <PageShell>
      {/* --- IDLE & LOADING STATES --- */}
      {(appState === "idle" || appState === "converting" || appState === "explaining") && (
        <div className="max-w-xl mx-auto w-full mt-12 transition-all duration-500">
          <UploadCard 
            onFileSelect={handleFileUpload} 
            status={appState} 
          />
        </div>
      )}

      {/* --- ERROR STATE --- */}
      {appState === "error" && (
        <div className="bg-red-50 text-red-700 p-6 rounded-xl text-center border border-red-200 max-w-xl mx-auto w-full mt-12">
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

      {/* --- SUCCESS STATE --- */}
      {appState === "success" && convertData && explainData && (
        <div className="space-y-6 animate-in fade-in zoom-in duration-500 relative">
          {/* Project Header */}
          <div className="flex justify-between items-center bg-white p-4 rounded-xl shadow-sm border border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="bg-green-100 p-2 rounded-lg text-green-600">
                <span className="text-xl">🌱</span>
              </div>
              <h2 className="text-xl font-bold text-slate-800">
                {convertData.project_name}
              </h2>
            </div>
            <button 
              onClick={resetApp}
              className="text-sm font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 py-2 px-4 rounded-lg transition-colors"
            >
              Convert Another Project
            </button>
          </div>

          {/* Warnings (if any) */}
          {convertData.warnings && convertData.warnings.length > 0 && (
             <WarningBanner warnings={convertData.warnings} />
          )}

          {/* Main Results Container (Full Width Now!) */}
          <div className="w-full items-start pb-32"> {/* Added pb-32 so the cat doesn't cover code at the bottom */}
            {/* Full Width Python Panel */}
            <div className="w-full flex flex-col h-full">
              <PythonPanel 
                code={convertData.python_code} 
                // Will wire this up next
                // onHintClick={(section) => setActiveSection(section)}
              />
              
              {/* COMMENTED OUT FOR NOW:
                <MappingPanel mappings={convertData.mappings} /> 
              */}
            </div>

            {/* COMMENTED OUT FOR NOW:
            <div className="h-full mt-6">
              <ExplanationsPanel explanations={explainData.explanations} />
            </div>
            */}
          </div>

          {/* Floating Tutor will go here */}
          {/* {activeSection && (
            <FloatingTutor 
              section={activeSection} 
              explanations={explainData.explanations} 
              onClose={() => setActiveSection(null)} 
            />
          )} */}
        </div>
      )}
    </PageShell>
  );
}