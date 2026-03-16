# =============================================================================
# AI Multimodal Tutor - Main Application Entry Point
# =============================================================================
# Phase: 1 - Project Setup & Infrastructure
# Purpose: FastAPI backend server setup with basic endpoints
# Version: 1.0.0
#
# Endpoints:
#   - GET  /health        : Health check
#   - GET  /              : API information
#   - POST /ask           : Text question (Phase 4-5)
#   - POST /ask/voice     : Voice question (Phase 4-5)
#   - POST /ask/upload    : Code/image upload (Phase 4-5)
#   - POST /ingest        : Trigger course ingestion (Phase 2)
# =============================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# =============================================================================
# FASTAPI APPLICATION SETUP
# =============================================================================

app = FastAPI(
    title="AI Multimodal Tutor API",
    description="""
    ## Overview
    AI Multimodal Tutor transforms a GitHub programming course into a live 
    AI-powered tutor using Vector DB + RAG + Gemini LLM.
    
    ## Features
    - Text, voice, and code/image input
    - Multimodal output (text, code, diagrams, voice)
    - RAG-powered answers from course content
    - Fallback to general LLM knowledge
    
    ## Phases
    - Phase 1: Project Setup (COMPLETE)
    - Phase 2: Backend Core Components
    - Phase 3: RAG Pipeline
    - Phase 4: LLM Integration
    - Phase 5: Frontend Development
    - Phase 6: Multimodal I/O Features
    - Phase 7: Integration & Testing
    - Phase 8: Deployment & Demo
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# =============================================================================
# CORS CONFIGURATION
# =============================================================================

# Get frontend URL from environment (default: localhost:3000)
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# ROOT ENDPOINTS
# =============================================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information
    
    Returns basic information about the API and current version.
    """
    return {
        "name": "AI Multimodal Tutor API",
        "version": "1.0.0",
        "status": "running",
        "phase": "Phase 1: Project Setup Complete",
        "docs": "/docs",
        "message": "Welcome to AI Multimodal Tutor! Phases 2-8 pending."
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Used to verify the API is running and healthy.
    Returns status of various components.
    """
    return {
        "status": "healthy",
        "phase": "Phase 1: Project Setup",
        "version": "1.0.0"
    }

# =============================================================================
# PLACEHOLDER ENDPOINTS (To be implemented in future phases)
# =============================================================================

@app.post("/ask", tags=["问答"])
async def ask_question(question: str):
    """
    Ask a text question
    
    Phase: 4-5 (RAG Pipeline + LLM Integration)
    
    Processes a text question and returns a multimodal answer
    grounded in the course content.
    """
    return {
        "message": "Endpoint not yet implemented",
        "phase": "Pending: Phase 4-5",
        "question": question
    }


@app.post("/ask/voice", tags=["问答"])
async def ask_voice():
    """
    Ask a voice question
    
    Phase: 6 (Multimodal I/O Features)
    
    Accepts voice input, processes it, and returns multimodal answer.
    """
    return {
        "message": "Endpoint not yet implemented",
        "phase": "Pending: Phase 6"
    }


@app.post("/ask/upload", tags=["问答"])
async def ask_upload():
    """
    Ask with code/image upload
    
    Phase: 6 (Multimodal I/O Features)
    
    Accepts code snippets or screenshots and returns multimodal answer.
    """
    return {
        "message": "Endpoint not yet implemented",
        "phase": "Pending: Phase 6"
    }


@app.post("/ingest", tags=["Ingestion"])
async def ingest_course():
    """
    Trigger course ingestion
    
    Phase: 2 (Backend - Core Components)
    
    Fetches GitHub course content and ingests into Vector DB.
    """
    return {
        "message": "Endpoint not yet implemented",
        "phase": "Pending: Phase 2"
    }


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler
    
    Catches any unhandled exceptions and returns a proper error response.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "phase": "Phase 1"
        }
    )


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )
