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
  };

  return (
    <PageShell>
      {/* State: Idle / Loading */}
      {(appState === "idle" || appState === "converting" || appState === "explaining") && (
        <div className="max-w-xl mx-auto w-full mt-12">
          <UploadCard 
            onFileSelect={handleFileUpload} 
            isLoading={appState === "converting" || appState === "explaining"} 
          />
          {appState === "converting" && <p className="text-center mt-4 text-slate-500 animate-pulse">Translating your blocks...</p>}
          {appState === "explaining" && <p className="text-center mt-4 text-slate-500 animate-pulse">Writing your explanations...</p>}
        </div>
      )}

      {/* State: Error */}
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

      {/* State: Success */}
      {appState === "success" && convertData && explainData && (
        <div className="space-y-6 fade-in">
          <div className="flex justify-between items-center bg-white p-4 rounded-xl shadow-sm border border-gray-100">
            <h2 className="text-xl font-bold text-green-700">Project: {convertData.project_name}</h2>
            <button 
              onClick={resetApp}
              className="text-sm font-semibold bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-4 rounded-lg transition-colors"
            >
              Convert Another Project
            </button>
          </div>

          {convertData.warnings && convertData.warnings.length > 0 && (
             <WarningBanner warnings={convertData.warnings} />
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
            {/* Left Column: Code and Mappings */}
            <div className="space-y-6 flex flex-col h-full">
              <PythonPanel code={convertData.python_code} />
              <MappingPanel mappings={convertData.mappings} />
            </div>

            {/* Right Column: Explanations */}
            <div className="h-full">
               {/* Assuming ExplanationsPanel takes an array of ExplanationSections */}
              <ExplanationsPanel explanations={explainData.explanations} />
            </div>
          </div>
        </div>
      )}
    </PageShell>
  );
}