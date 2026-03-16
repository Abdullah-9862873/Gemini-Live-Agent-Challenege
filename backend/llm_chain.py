# =============================================================================
# AI Multimodal Tutor - LLM Chain (Gemini Integration)
# =============================================================================
# Phase: 4 - LLM Integration
# Purpose: Gemini LLM integration for answer generation
# Version: 4.0.0
# =============================================================================

import google.generativeai as genai
from typing import Dict, Any, Optional, List
import logging
from config import settings
from prompt_templates import PromptBuilder, PromptTemplates
from rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMChain:
    """
    LLM Chain for generating answers using Gemini.
    
    This class handles:
    - Gemini API configuration
    - Prompt construction with RAG context
    - Answer generation
    - Error handling and retries
    - Fallback to general knowledge
    
    Attributes:
        model: Gemini model instance
        model_name: Name of the Gemini model
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the LLM chain with Gemini.
        
        Args:
            model_name: Name of the Gemini model (uses config default if None)
        """
        # Configure Gemini API
        genai.configure(api_key=settings.gemini_api_key)
        
        self.model_name = model_name or settings.gemini_model
        self.model = None
        
        # Initialize model
        self._init_model()
    
    def _init_model(self) -> None:
        """
        Initialize the Gemini model.
        """
        try:
            logger.info(f"Initializing Gemini model: {self.model_name}")
            self.model = genai.GenerativeModel(self.model_name)
            logger.info("Gemini model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            raise
    
    def generate_answer(
        self,
        question: str,
        context: str = "",
        has_context: bool = True,
        prompt_type: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Dict[str, Any]:
        """
        Generate an answer using Gemini.
        
        Args:
            question: User's question
            context: Retrieved context from RAG pipeline
            has_context: Whether relevant context is available
            prompt_type: Type of prompt (default, code, step_by_step)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
        
        Returns:
            Dictionary with generated answer and metadata
        
        Example:
            >>> llm = LLMChain()
            >>> result = llm.generate_answer(
            ...     question="What is merge sort?",
            ...     context="Merge sort is a divide-and-conquer algorithm...",
            ...     has_context=True
            ... )
            >>> print(result["answer"])
            "Merge sort works by..."
        """
        logger.info(f"Generating answer for question: {question[:50]}...")
        
        # Build prompts
        builder = PromptBuilder()
        builder.set_question(question)
        builder.set_context(context)
        builder.set_prompt_type(prompt_type)
        
        prompts = builder.build()
        system_prompt = prompts["system"]
        user_prompt = prompts["user"]
        
        try:
            # Generate content
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
            
            response = self.model.generate_content(
                contents=[
                    {"role": "user", "parts": [{"text": user_prompt}]}
                ],
                generation_config=generation_config
            )
            
            # Extract answer
            answer_text = response.text
            
            logger.info(f"Answer generated successfully ({len(answer_text)} chars)")
            
            return {
                "answer": answer_text,
                "has_context": has_context,
                "context_used": bool(context),
                "model": self.model_name,
                "status": "success"
            }
        
        except Exception as e:
            logger.error(f"Failed to generate answer: {e}")
            return {
                "answer": f"I apologize, but I encountered an error while generating the answer: {str(e)}",
                "has_context": has_context,
                "context_used": bool(context),
                "model": self.model_name,
                "status": "error",
                "error": str(e)
            }
    
    def generate_with_rag(
        self,
        question: str,
        top_k: int = None,
        threshold: float = None,
        prompt_type: str = "default"
    ) -> Dict[str, Any]:
        """
        Generate answer using RAG pipeline + LLM.
        
        This is a convenience method that combines RAG retrieval
        with LLM generation.
        
        Args:
            question: User's question
            top_k: Number of context results
            threshold: Similarity threshold
            prompt_type: Type of prompt
        
        Returns:
            Dictionary with answer, context, and metadata
        """
        # First, get context from RAG
        rag = RAGPipeline(top_k=top_k, threshold=threshold)
        rag_result = rag.run(query=question)
        
        # Extract context
        context = rag_result.get("context_text", "")
        has_relevant_context = rag_result.get("has_relevant_context", False)
        contexts = rag_result.get("contexts", [])
        
        # Generate answer
        answer_result = self.generate_answer(
            question=question,
            context=context,
            has_context=has_relevant_context,
            prompt_type=prompt_type
        )
        
        # Combine results
        sources = list(set([ctx.get("source", "") for ctx in contexts if ctx.get("source")]))
        
        return {
            "question": question,
            "answer": answer_result.get("answer", ""),
            "has_context": has_relevant_context,
            "context_used": bool(context),
            "sources": sources,
            "num_contexts": len(contexts),
            "top_score": rag_result.get("top_score", 0.0),
            "model": self.model_name,
            "status": answer_result.get("status", "error")
        }
    
    def generate_followup(
        self,
        question: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Generate answer with conversation history.
        
        Args:
            question: Current question
            conversation_history: Previous Q&A pairs
        
        Returns:
            Dictionary with generated answer
        """
        # Build conversation context
        context_parts = []
        
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages
                role = msg.get("role", "user")
                content = msg.get("content", "")
                context_parts.append(f"{role}: {content}")
        
        # Add current question
        context_parts.append(f"user: {question}")
        
        full_prompt = "\n\n".join(context_parts)
        
        try:
            response = self.model.generate_content(
                contents=[{"role": "user", "parts": [{"text": full_prompt}]}]
            )
            
            return {
                "answer": response.text,
                "status": "success"
            }
        
        except Exception as e:
            logger.error(f"Failed to generate followup: {e}")
            return {
                "answer": f"Error: {str(e)}",
                "status": "error"
            }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

llm_chain = LLMChain()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_answer(
    question: str,
    context: str = "",
    has_context: bool = True
) -> Dict[str, Any]:
    """
    Generate an answer using Gemini.
    
    Convenience function.
    
    Args:
        question: User's question
        context: Retrieved context
        has_context: Whether context is available
    
    Returns:
        Generated answer dictionary
    """
    chain = LLMChain()
    return chain.generate_answer(
        question=question,
        context=context,
        has_context=has_context
    )


def ask_with_rag(
    question: str,
    top_k: int = None,
    threshold: float = None
) -> Dict[str, Any]:
    """
    Ask a question using RAG + LLM.
    
    Convenience function.
    
    Args:
        question: User's question
        top_k: Number of context results
        threshold: Similarity threshold
    
    Returns:
        Full answer with context
    """
    chain = LLMChain()
    return chain.generate_with_rag(
        question=question,
        top_k=top_k,
        threshold=threshold
    )
