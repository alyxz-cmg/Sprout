/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        vscode: {
          bg: '#1e1e1e',
          sidebar: '#252526',
          tabActive: '#1e1e1e',
          accent: '#007acc',
          border: '#333333',
          text: '#cccccc'
        }
      }
    },
  },
  plugins: [],
}