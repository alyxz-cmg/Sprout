import React from "react";
import sproutCat from "../../assets/sprout-cat.png";

interface FileDropzoneProps {
  onFileSelect: (file: File) => void;
  disabled?: boolean;
}

export function FileDropzone({ onFileSelect, disabled = false }: FileDropzoneProps) {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <div className={`text-center p-12 border-4 border-dashed rounded-3xl transition-colors ${
      disabled ? "border-slate-200 bg-slate-50 cursor-not-allowed" : "border-green-300 bg-green-50 hover:bg-green-100 cursor-pointer"
    }`}>
      <div className="flex justify-center mb-4">
        <img 
          src={sproutCat} 
          alt="Sprout Cat Mascot" 
          className={`w-48 h-48 object-contain ${disabled ? "grayscale opacity-50" : ""}`}
        />
      </div>
      
      <h2 className="text-2xl font-extrabold text-green-800 mb-2">Upload your Scratch Game!</h2>
      <p className="text-green-600 mb-6 font-medium">Drop your .sb3 file here, or click to browse.</p>
      
      <label className={`relative inline-flex items-center justify-center px-8 py-3 text-base font-bold text-white transition-all bg-green-500 rounded-full shadow-lg ${disabled ? "opacity-50" : "hover:bg-green-600 hover:-translate-y-1"}`}>
        Choose File
        <input 
          type="file" 
          accept=".sb3" 
          onChange={handleFileChange}
          disabled={disabled}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
      </label>
    </div>
  );
}