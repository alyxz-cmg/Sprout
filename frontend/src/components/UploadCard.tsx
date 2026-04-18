import { FileDropzone } from "./upload/FileDropzone";

interface UploadCardProps {
  onFileSelect: (file: File) => void;
  status: "idle" | "converting" | "explaining" | "success" | "error";
}

export default function UploadCard({ onFileSelect, status }: UploadCardProps) {
  const isLoading = status === "converting" || status === "explaining";

  return (
    <div className="bg-white p-8 rounded-2xl shadow-sm border border-green-100 text-center">   
      <FileDropzone onFileSelect={onFileSelect} disabled={isLoading} />
      
      {status === "converting" && (
        <p className="text-green-600 mt-4 animate-pulse font-medium">
          🌱 Planting your code...
        </p>
      )}
      
      {status === "explaining" && (
        <p className="text-blue-600 mt-4 animate-pulse font-medium">
          🦉 Writing your guide...
        </p>
      )}
    </div>
  );
}