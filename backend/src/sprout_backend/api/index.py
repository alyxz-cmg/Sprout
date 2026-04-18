from src.sprout_backend.main import app
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    "https://sprout-frontend-sandy.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)