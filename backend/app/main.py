"""
FastAPI Main Application
Emotion-Driven Decision System Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routers import emotion, decision
from app.models import facial_model, speech_model, text_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown
    """
    # Startup: Load models
    print("Loading emotion detection models...")
    facial_loaded = facial_model.load_model()
    speech_loaded = speech_model.load_model()
    text_loaded = text_model.load_model()
    
    if facial_loaded:
        print("✓ Facial emotion model loaded")
    else:
        print("✗ Facial emotion model not loaded")
    
    if speech_loaded:
        print("✓ Speech emotion model loaded")
    else:
        print("✗ Speech emotion model not loaded")
        
    if text_loaded:
        print("✓ Text emotion model loaded")
    else:
        print("✗ Text emotion model not loaded")
    
    print("Server ready!")
    
    yield
    
    # Shutdown
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Multimodal emotion detection and decision support system",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(emotion.router, prefix=settings.api_prefix)
app.include_router(decision.router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Emotion-Driven Decision System API",
        "version": settings.version,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "facial_model_loaded": facial_model.model_loaded,
        "speech_model_loaded": speech_model.model_loaded,
        "text_model_loaded": text_model.model_loaded
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
