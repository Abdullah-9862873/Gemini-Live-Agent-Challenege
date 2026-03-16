# =============================================================================
# AI Multimodal Tutor - Backend Package
# =============================================================================
# Phase: 4 - LLM Integration
# Purpose: Package initialization file
# Version: 4.0.0
# =============================================================================

"""
AI Multimodal Tutor Backend

This package contains all backend components:
- config: Configuration management
- vector_db: Pinecone Vector DB operations
- embeddings: Sentence transformer embeddings
- github_ingest: GitHub repository ingestion (public repos only)
- ingestion_pipeline: Complete ingestion workflow
- rag_pipeline: Retrieval-Augmented Generation pipeline
- prompt_templates: Prompt templates for RAG + LLM
- llm_chain: Gemini LLM integration
- multimodal: Multimodal output generator
- tts_service: Text-to-Speech service
"""

__version__ = "4.0.0"
