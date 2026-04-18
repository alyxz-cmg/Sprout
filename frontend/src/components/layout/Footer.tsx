export default function Footer() {
  return (
    <footer className="bg-transparent text-gray-500/80 p-8 text-sm">
      <div className="container mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
        
        {/* Left Aligned: Copyright */}
        <div className="order-2 md:order-1 font-medium">
          © 2026 Sprout. All rights reserved.
        </div>

        {/* Right Aligned: Links */}
        <div className="order-3 flex items-center space-x-4">
          <a 
            href="https://github.com/alyxz-cmg/Sprout" 
            target="_blank" 
            rel="noopener noreferrer"
            className="hover:text-green-600 transition-colors font-semibold flex items-center gap-1"
          >
            GitHub
          </a>
        </div>
        
      </div>
    </footer>
  );
}