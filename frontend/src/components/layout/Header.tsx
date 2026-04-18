import { Sprout } from "lucide-react";

export default function Header() {
  return (
    <header className="bg-green-600 text-white p-4 shadow-md flex items-center justify-between">
      <div className="flex items-center gap-2">
        <Sprout className="w-8 h-8" />
        <h1 className="text-2xl font-bold tracking-wide">Sprout</h1>
      </div>
      <p className="text-green-100 font-medium hidden sm:block">
        Scratch to Python Converter
      </p>
    </header>
  );
}