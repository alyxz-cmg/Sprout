import FileDropzone from "./upload/FileDropzone";

interface UploadCardProps {
  onFileSelect: (file: File) => void;
  isLoading?: boolean;
}

export default function UploadCard({ onFileSelect, isLoading }: UploadCardProps) {
  return (
    <div className="bg-white p-8 rounded-2xl shadow-sm border border-green-100 text-center">
      <h2 className="text-xl font-semibold mb-6 text-gray-800">
        Upload your Scratch Project (.sb3)
      </h2>
      <FileDropzone onFileSelect={onFileSelect} disabled={isLoading} />
      {isLoading && (
        <p className="text-green-600 mt-4 animate-pulse font-medium">
          Planting your code...
        </p>
      )}
    </div>
  );
}