# =============================================================================
# AI Multimodal Tutor - Multimodal Output Generator
# =============================================================================
# Phase: 4 - LLM Integration (Multimodal Features)
# Purpose: Generate multimodal outputs (text, code, diagrams)
# Version: 4.0.0
# =============================================================================

import google.generativeai as genai
from typing import Dict, Any, Optional, List
import re
import logging
from backend.config import settings
from backend.llm_chain import LLMChain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultimodalGenerator:
    """
    Multimodal Output Generator.
    
    This class generates different types of outputs:
    - Text explanations
    - Code snippets
    - Diagrams (via Gemini)
    - Structured responses
    
    Attributes:
        llm: LLMChain instance for generating content
    """
    
    def __init__(self):
        """Initialize the multimodal generator."""
        self.llm = LLMChain()
        
        # Configure Gemini for vision (if needed)
        genai.configure(api_key=settings.gemini_api_key)
    
    def extract_code_blocks(self, text: str) -> List[Dict[str, str]]:
        """
        Extract code blocks from text.
        
        Args:
            text: Text containing code blocks
        
        Returns:
            List of code blocks with language and code
        """
        code_blocks = []
        
        # Match markdown code blocks
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for language, code in matches:
            code_blocks.append({
                "language": language or "text",
                "code": code.strip()
            })
        
        return code_blocks
    
    def format_code_response(self, code: str, language: str = "python") -> str:
        """
        Format code for response.
        
        Args:
            code: Code string
            language: Programming language
        
        Returns:
            Formatted code block
        """
        return f"```{language}\n{code}\n```"
    
    def generate_diagram_prompt(self, topic: str, context: str = "") -> str:
        """
        Generate a prompt for creating a diagram.
        
        Args:
            topic: Topic to diagram
            context: Additional context
        
        Returns:
            Prompt for Gemini to generate diagram description
        """
        prompt = f"""Create a clear diagram description for explaining: {topic}

Context: {context}

Provide:
1. A brief description of what the diagram should show
2. Key elements to include
3. Labels and annotations

Keep it simple and educational."""
        return prompt
    
    def extract_structured_response(self, text: str) -> Dict[str, Any]:
        """
        Extract structured parts from response.
        
        Args:
            text: Raw response text
        
        Returns:
            Dictionary with extracted parts
        """
        result = {
            "text": text,
            "has_code": False,
            "code_blocks": [],
            "steps": [],
            "explanation": text
        }
        
        # Extract code blocks
        code_blocks = self.extract_code_blocks(text)
        if code_blocks:
            result["has_code"] = True
            result["code_blocks"] = code_blocks
        
        # Extract steps (numbered lists)
        step_pattern = r'(\d+)\.\s+(.+?)(?=\n\d+\.|$)'
        steps = re.findall(step_pattern, text, re.DOTALL)
        if steps:
            result["steps"] = [step[1].strip() for step in steps]
        
        return result
    
    def generate_full_response(
        self,
        question: str,
        answer: str,
        sources: List[str] = None,
        include_diagram: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a full multimodal response.
        
        Args:
            question: User's question
            answer: Generated answer
            sources: List of source files
            include_diagram: Whether to include diagram prompt
        
        Returns:
            Complete multimodal response dictionary
        """
        # Extract structured parts
        structured = self.extract_structured_response(answer)
        
        response = {
            "question": question,
            "answer": answer,
            "explanation": structured.get("explanation", ""),
            "has_code": structured.get("has_code", False),
            "code_blocks": structured.get("code_blocks", []),
            "steps": structured.get("steps", []),
            "sources": sources or [],
            "has_diagram": include_diagram,
            "diagram_prompt": None
        }
        
        # Generate diagram prompt if requested
        if include_diagram:
            response["diagram_prompt"] = self.generate_diagram_prompt(
                topic=question,
                context=answer[:500]
            )
        
        return response
    
    def generate_code_focused(
        self,
        question: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Generate a code-focused response.
        
        Args:
            question: User's question
            context: RAG context
        
        Returns:
            Response with code focus
        """
        result = self.llm.generate_answer(
            question=question,
            context=context,
            has_context=bool(context),
            prompt_type="code"
        )
        
        answer = result.get("answer", "")
        code_blocks = self.extract_code_blocks(answer)
        
        return {
            "question": question,
            "answer": answer,
            "has_code": bool(code_blocks),
            "code_blocks": code_blocks,
            "status": result.get("status", "error")
        }
    
    def generate_step_by_step(
        self,
        question: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Generate a step-by-step response.
        
        Args:
            question: User's question
            context: RAG context
        
        Returns:
            Response with steps
        """
        result = self.llm.generate_answer(
            question=question,
            context=context,
            has_context=bool(context),
            prompt_type="step_by_step"
        )
        
        answer = result.get("answer", "")
        
        # Extract steps
        step_pattern = r'(\d+)\.\s+(.+?)(?=\n\d+\.|$)'
        steps = re.findall(step_pattern, answer, re.DOTALL)
        
        return {
            "question": question,
            "answer": answer,
            "steps": [step[1].strip() for step in steps],
            "status": result.get("status", "error")
        }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

multimodal_generator = MultimodalGenerator()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_response(
    question: str,
    answer: str,
    sources: List[str] = None
) -> Dict[str, Any]:
    """
    Generate a full multimodal response.
    
    Convenience function.
    
    Args:
        question: User's question
        answer: Generated answer
        sources: List of sources
    
    Returns:
        Multimodal response
    """
    generator = MultimodalGenerator()
    return generator.generate_full_response(question, answer, sources)


def extract_code(text: str) -> List[Dict[str, str]]:
    """
    Extract code blocks from text.
    
    Convenience function.
    
    Args:
        text: Text containing code
    
    Returns:
        List of code blocks
    """
    generator = MultimodalGenerator()
    return generator.extract_code_blocks(text)
