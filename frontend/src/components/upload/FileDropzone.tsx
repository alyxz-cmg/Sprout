import React, { useState } from "react";
import sproutCat from "../../assets/sprout-cat.png";

interface FileDropzoneProps {
  onFileSelect: (file: File) => void;
  disabled?: boolean;
}

export function FileDropzone({ onFileSelect, disabled = false }: FileDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.name.endsWith('.sb3')) {
      onFileSelect(file);
    } else if (file) {
      alert("Please upload a valid .sb3 Scratch project file.");
    }
  };

  // --- Drag & Drop Handlers ---
  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!disabled) setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!disabled) setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (disabled) return;
    
    setIsDragging(false);

    const file = e.dataTransfer.files?.[0];
    if (file && file.name.endsWith('.sb3')) {
      onFileSelect(file);
    } else if (file) {
      alert("Please upload a valid .sb3 Scratch project file.");
    }
  };

  return (
    <div 
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`text-center p-12 border-4 border-dashed rounded-3xl transition-all duration-200 ${
        disabled 
          ? "border-slate-200 bg-slate-50 cursor-not-allowed" 
          : isDragging 
            ? "border-green-500 bg-green-100 scale-[1.02]"
            : "border-green-300 bg-green-50 hover:bg-green-100 cursor-pointer"
      }`}
    >
      <div className="flex justify-center mb-4 pointer-events-none">
        <img 
          src={sproutCat} 
          alt="Sprout Cat Mascot" 
          className={`w-48 h-48 object-contain transition-transform duration-300 ${
            disabled ? "grayscale opacity-50" : isDragging ? "scale-110" : ""
          }`}
        />
      </div>
      
      <h2 className="text-2xl font-extrabold text-green-800 mb-2 pointer-events-none">
        {isDragging ? "Drop it!" : "Upload your Scratch Game!"}
      </h2>
      <p className="text-green-600 mb-6 font-medium pointer-events-none">
        Drop your .sb3 file here, or click to browse.
      </p>
      
      <label className={`relative inline-flex items-center justify-center px-8 py-3 text-base font-bold text-white transition-all bg-green-500 rounded-full shadow-lg ${
        disabled ? "opacity-50 cursor-not-allowed" : "hover:bg-green-600 hover:-translate-y-1 cursor-pointer"
      }`}>
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