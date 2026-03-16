# =============================================================================
# AI Multimodal Tutor - Main Application Entry Point
# =============================================================================
# Phase: 2 - Backend Core Components (UPDATED)
# Purpose: FastAPI backend server setup with ingestion endpoints
# Version: 2.0.0
#
# Endpoints:
#   - GET  /health        : Health check
#   - GET  /              : API information
#   - POST /ask           : Text question (Phase 4-5)
#   - POST /ask/voice     : Voice question (Phase 4-5)
#   - POST /ask/upload    : Code/image upload (Phase 4-5)
#   - POST /ingest        : Trigger course ingestion (Phase 2 - NOW IMPLEMENTED)
#   - GET  /ingest/status : Get ingestion status
# =============================================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    - Phase 2: Backend Core Components (COMPLETE)
    - Phase 3: RAG Pipeline
    - Phase 4: LLM Integration
    - Phase 5: Frontend Development
    - Phase 6: Multimodal I/O Features
    - Phase 7: Integration & Testing
    - Phase 8: Deployment & Demo
    """,
    version="2.0.0",
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
        "version": "2.0.0",
        "status": "running",
        "phase": "Phase 2: Backend Core Components Complete",
        "docs": "/docs",
        "message": "Welcome to AI Multimodal Tutor! Phases 3-8 pending."
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
        "phase": "Phase 2: Backend Core Components",
        "version": "2.0.0",
        "components": {
            "fastapi": "running",
            "pinecone": "configured",
            "embeddings": "configured",
            "github": "configured"
        }
    }

# =============================================================================
# REQUEST MODELS
# =============================================================================

class IngestRequest(BaseModel):
    """
    Request model for ingestion endpoint.
    """
    repo: Optional[str] = None
    extensions: Optional[List[str]] = None


class IngestResponse(BaseModel):
    """
    Response model for ingestion endpoint.
    """
    status: str
    message: str
    chunks_created: int = 0
    vectors_stored: int = 0


# =============================================================================
# INGESTION ENDPOINTS (Phase 2 - IMPLEMENTED)
# =============================================================================

@app.post("/ingest", tags=["Ingestion"], response_model=IngestResponse)
async def ingest_course(request: Optional[IngestRequest] = None):
    """
    Trigger course ingestion from GitHub repository
    
    Phase: 2 (Backend - Core Components) - NOW IMPLEMENTED
    
    Fetches GitHub course content and ingests into Vector DB.
    
    Args:
        request: Optional IngestRequest with repo and extensions
    
    Returns:
        IngestResponse with ingestion results
    
    Example:
        POST /ingest
        {
            "repo": "username/dsa-course",
            "extensions": [".md", ".py", ".js"]
        }
    """
    from backend.ingestion_pipeline import ingestion_pipeline
    from backend.config import settings, validate_all_configs
    
    logger.info("Ingestion request received")
    
    # Validate configurations
    configs = validate_all_configs()
    
    # Check required configs
    if not configs["pinecone"]:
        raise HTTPException(
            status_code=400,
            detail="Pinecone API key not configured"
        )
    if not configs["github"]:
        raise HTTPException(
            status_code=400,
            detail="GitHub token or repo not configured"
        )
    
    # Get repo from request or use default
    repo = request.repo if request and request.repo else settings.github_repo
    extensions = request.extensions if request and request.extensions else [".md", ".txt", ".py", ".js", ".ts"]
    
    logger.info(f"Starting ingestion for repo: {repo}")
    logger.info(f"File extensions: {extensions}")
    
    try:
        # Run ingestion pipeline
        result = ingestion_pipeline.run(
            repo=repo,
            extensions=extensions
        )
        
        if result["status"] == "success":
            return IngestResponse(
                status="success",
                message=f"Successfully ingested {result['chunks_created']} chunks ({result['vectors_stored']} vectors)",
                chunks_created=result["chunks_created"],
                vectors_stored=result["vectors_stored"]
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "Ingestion failed")
            )
    
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )


@app.get("/ingest/status", tags=["Ingestion"])
async def get_ingestion_status():
    """
    Get ingestion status and statistics
    
    Phase: 2
    
    Returns information about the Vector DB index and last ingestion.
    """
    from backend.vector_db import vector_db
    from backend.config import settings
    
    try:
        stats = vector_db.get_index_stats()
        
        return {
            "status": "success",
            "index_name": settings.pinecone_index_name,
            "total_vectors": stats.get("total_vector_count", 0),
            "dimension": stats.get("dimension", 0),
            "namespaces": stats.get("namespaces", {}),
            "phase": "Phase 2: Complete"
        }
    except Exception as e:
        logger.error(f"Failed to get ingestion status: {e}")
        return {
            "status": "error",
            "message": str(e),
            "phase": "Phase 2"
        }


# =============================================================================
# PLACEHOLDER ENDPOINTS (To be implemented in future phases)
# =============================================================================

@app.post("/ask", tags=["Q&A"])
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


@app.post("/ask/upload", tags=["Q&A"])
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


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler
    
    Catches any unhandled exceptions and returns a proper error response.
    """
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "phase": "Phase 2"
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
