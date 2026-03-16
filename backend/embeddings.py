# =============================================================================
# AI Multimodal Tutor - Embedding Model Integration
# =============================================================================
# Phase: 2 - Backend Core Components
# Purpose: Generate embeddings using sentence-transformers
# Version: 2.0.0
# =============================================================================

from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np
import logging
from backend.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingModel:
    """
    Sentence Transformer Embedding Model Manager.
    
    This class handles the embedding model for converting text to vectors.
    Uses sentence-transformers library with the configured model.
    
    Attributes:
        model: SentenceTransformer model instance
        model_name: Name of the embedding model
        dimension: Vector dimension of the embeddings
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the embedding model.
        
        Args:
            model_name: Name of the sentence-transformers model
                       (uses config default if None)
        """
        self.model_name = model_name or settings.embedding_model
        self.model = None
        self.dimension = None
        
        # Load model on initialization
        self._load_model()
    
    def _load_model(self) -> None:
        """
        Load the sentence-transformers model.
        
        This may take a few seconds on first load as the model
        is downloaded from Hugging Face.
        """
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
            logger.info(f"Model loaded successfully. Dimension: {self.dimension}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    
    def encode(
        self,
        texts: Union[str, List[str]],
        batch_size: int = 32,
        show_progress: bool = False
    ) -> np.ndarray:
        """
        Encode text(s) into embeddings.
        
        Args:
            texts: Single text string or list of text strings
            batch_size: Batch size for encoding (default: 32)
            show_progress: Whether to show encoding progress
        
        Returns:
            NumPy array of embeddings
        
        Example:
            >>> embeddings = embedding_model.encode("What is merge sort?")
            >>> print(embeddings.shape)  # (384,)
            >>> 
            >>> texts = ["What is merge sort?", "Explain quicksort"]
            >>> embeddings = embedding_model.encode(texts)
            >>> print(embeddings.shape)  # (2, 384)
        """
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=show_progress,
                convert_to_numpy=True
            )
            return embeddings
        except Exception as e:
            logger.error(f"Failed to encode texts: {e}")
            raise
    
    def encode_single(self, text: str) -> List[float]:
        """
        Encode a single text into a list of floats.
        
        This is a convenience method that returns a list instead of numpy array.
        
        Args:
            text: Single text string to encode
        
        Returns:
            List of floats representing the embedding vector
        
        Example:
            >>> embedding = embedding_model.encode_single("What is merge sort?")
            >>> print(len(embedding))  # 384
        """
        embedding = self.encode(texts=[text])
        return embedding[0].tolist()
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Encode multiple texts into a list of embedding vectors.
        
        Args:
            texts: List of text strings to encode
        
        Returns:
            List of embedding vectors (each a list of floats)
        
        Example:
            >>> embeddings = embedding_model.encode_batch([
            ...     "What is merge sort?",
            ...     "Explain quicksort",
            ...     "How does binary search work?"
            ... ])
            >>> print(len(embeddings))  # 3
            >>> print(len(embeddings[0]))  # 384
        """
        embeddings = self.encode(texts=texts, show_progress=True)
        return embeddings.tolist()
    
    def get_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors.
        
        Returns:
            Integer representing the embedding dimension
        """
        return self.dimension
    
    def get_model_name(self) -> str:
        """
        Get the name of the embedding model.
        
        Returns:
            String representing the model name
        """
        return self.model_name


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

# Create a singleton instance for use throughout the application
embedding_model = EmbeddingModel()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_embedding(text: str) -> List[float]:
    """
    Get embedding for a single text.
    
    Convenience function that uses the singleton embedding_model.
    
    Args:
        text: Text to embed
    
    Returns:
        List of floats representing the embedding
    """
    return embedding_model.encode_single(text)


def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Get embeddings for multiple texts.
    
    Convenience function that uses the singleton embedding_model.
    
    Args:
        texts: List of texts to embed
    
    Returns:
        List of embedding vectors (each a list of floats)
    """
    return embedding_model.encode_batch(texts)
