# 🌱 Sprout

Sprout is a kid-friendly app that turns Scratch `.sb3` projects into readable Python code and explains the conversion in simple, encouraging language!

## The Vision
Make the jump from Scratch to Python feel like leveling up in a game: easy to start, fun to explore, and rewarding to complete.

## Tech Stack
* **Frontend**: React, TypeScript, Vite, TailwindCSS
* **Backend**: Python, FastAPI
* **AI Layer**: OpenAI (GPT-4o) - *Strictly for educational explanations*

## View Status
https://stats.uptimerobot.com/XJcTACqmvk

## Local Development

### 1. Clone & Setup
Ensure you have `pnpm` and `python >= 3.10` installed.

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt # (Ensure fastapi, uvicorn, pydantic, openai are installed)

# Set your OpenAI key
export OPENAI_API_KEY="your-key-here"

# Run the dev server
uvicorn src.sprout_backend.main:app --reload
