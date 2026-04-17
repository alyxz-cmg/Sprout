from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .api.routes import convert, explain
from .core.exceptions import SproutBaseException

app = FastAPI(
    title="Sprout API",
    description="Backend for converting Scratch projects to Python with friendly explanations.",
    version="1.0.0"
)

# Allow CORS for the frontend (Vite defaults to 5173, Vercel will have its own domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler for our custom exceptions to ensure clean JSON responses
@app.exception_handler(SproutBaseException)
async def sprout_exception_handler(request: Request, exc: SproutBaseException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )

# Basic health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Sprout API is ready to grow!"}

# Include routers
app.include_router(convert.router, prefix="/api", tags=["Convert"])
app.include_router(explain.router, prefix="/api", tags=["Explain"])