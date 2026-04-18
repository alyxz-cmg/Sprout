import React from "react";
import Header from "./Header";
import Footer from "./Footer";

export default function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50 font-sans">
      <Header />
      <main className="flex-grow container mx-auto p-4 max-w-5xl flex flex-col gap-6 w-full">
        {children}
      </main>
      <Footer />
    </div>
  );
}