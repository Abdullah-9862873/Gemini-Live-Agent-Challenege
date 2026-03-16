# =============================================================================
# AI Multimodal Tutor - Vector Database (Pinecone) Operations
# =============================================================================
# Phase: 2 - Backend Core Components
# Purpose: Pinecone Vector DB connection and CRUD operations
# Version: 2.0.0
# =============================================================================

from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any, Optional
import logging
from backend.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorDB:
    """
    Pinecone Vector Database Manager.
    
    This class handles all interactions with Pinecone including:
    - Index creation and management
    - Vector upsert (insert/update)
    - Vector query (similarity search)
    - Vector deletion
    
    Attributes:
        pinecone_client: Pinecone client instance
        index: Active Pinecone index
        index_name: Name of the current index
    """
    
    def __init__(self):
        """
        Initialize Pinecone client and connect to index.
        
        Sets up the Pinecone client using the API key from config
        and connects to the specified index.
        """
        # Initialize Pinecone client
        self.pinecone_client = Pinecone(
            api_key=settings.pinecone_api_key
        )
        
        self.index_name = settings.pinecone_index_name
        self.index = None
        
        # Connect to index on initialization
        self._connect_to_index()
    
    def _connect_to_index(self) -> None:
        """
        Connect to the Pinecone index.
        
        If the index doesn't exist, it will be created.
        """
        # Check if index exists
        existing_indexes = self.pinecone_client.list_indexes()
        index_names = [idx.name for idx in existing_indexes]
        
        if self.index_name not in index_names:
            logger.info(f"Index '{self.index_name}' not found. Creating new index...")
            self._create_index()
        else:
            logger.info(f"Connecting to existing index: {self.index_name}")
            self.index = self.pinecone_client.Index(self.index_name)
        
        # Verify connection
        self._verify_connection()
    
    def _create_index(self, dimension: int = 384) -> None:
        """
        Create a new Pinecone index.
        
        Args:
            dimension: Vector dimension (default: 384 for all-MiniLM-L6-v2)
        """
        # Create index with serverless spec (cost-effective)
        self.pinecone_client.create_index(
            name=self.index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        
        logger.info(f"Index '{self.index_name}' created successfully")
        
        # Connect to newly created index
        self.index = self.pinecone_client.Index(self.index_name)
    
    def _verify_connection(self) -> bool:
        """
        Verify connection to the index.
        
        Returns:
            True if connection is successful, False otherwise.
        """
        try:
            stats = self.index.describe_index_stats()
            logger.info(f"Index stats: {stats}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to index: {e}")
            return False
    
    def upsert_vectors(
        self,
        vectors: List[Dict[str, Any]],
        namespace: str = ""
    ) -> Dict[str, Any]:
        """
        Insert or update vectors in the index.
        
        Args:
            vectors: List of vectors with id, values, and metadata
                    Format: [{"id": "vec1", "values": [...], "metadata": {...}}]
            namespace: Optional namespace for the vectors
        
        Returns:
            Dictionary with upsert results
        
        Example:
            >>> vectors = [
            ...     {
            ...         "id": "chunk_1",
            ...         "values": [0.1, 0.2, ...],
            ...         "metadata": {"text": "content", "source": "README.md"}
            ...     }
            ... ]
            >>> result = vector_db.upsert_vectors(vectors)
        """
        try:
            result = self.index.upsert(
                vectors=vectors,
                namespace=namespace
            )
            logger.info(f"Upserted {len(vectors)} vectors")
            return result
        except Exception as e:
            logger.error(f"Failed to upsert vectors: {e}")
            raise
    
    def query_vectors(
        self,
        query_vector: List[float],
        top_k: int = 5,
        include_metadata: bool = True,
        include_values: bool = False,
        namespace: str = "",
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query the index for similar vectors.
        
        Args:
            query_vector: The query embedding vector
            top_k: Number of results to return (default: 5)
            include_metadata: Whether to include metadata in results
            include_values: Whether to include vector values in results
            namespace: Optional namespace to search
            filter_dict: Optional filter for metadata
        
        Returns:
            Dictionary with query results including matches and scores
        
        Example:
            >>> query_vector = [0.1, 0.2, ...]
            >>> results = vector_db.query_vectors(query_vector, top_k=3)
            >>> for match in results['matches']:
            ...     print(f"Score: {match['score']}, Text: {match['metadata']['text']}")
        """
        try:
            result = self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=include_metadata,
                include_values=include_values,
                namespace=namespace,
                filter=filter_dict
            )
            return result
        except Exception as e:
            logger.error(f"Failed to query vectors: {e}")
            raise
    
    def delete_vectors(
        self,
        ids: List[str],
        namespace: str = ""
    ) -> Dict[str, Any]:
        """
        Delete vectors from the index.
        
        Args:
            ids: List of vector IDs to delete
            namespace: Optional namespace
        
        Returns:
            Dictionary with delete results
        """
        try:
            result = self.index.delete(
                ids=ids,
                namespace=namespace
            )
            logger.info(f"Deleted {len(ids)} vectors")
            return result
        except Exception as e:
            logger.error(f"Failed to delete vectors: {e}")
            raise
    
    def delete_all_vectors(self, namespace: str = "") -> None:
        """
        Delete all vectors from the index.
        
        Args:
            namespace: Optional namespace to clear
        """
        try:
            self.index.delete(delete_all=True, namespace=namespace)
            logger.info("All vectors deleted from index")
        except Exception as e:
            logger.error(f"Failed to delete all vectors: {e}")
            raise
    
    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the index.
        
        Returns:
            Dictionary with index statistics (dimension, total vectors, etc.)
        """
        try:
            stats = self.index.describe_index_stats()
            return stats
        except Exception as e:
            logger.error(f"Failed to get index stats: {e}")
            raise


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

# Create a singleton instance for use throughout the application
vector_db = VectorDB()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_relevant_context(
    query_embedding: List[float],
    top_k: int = None,
    threshold: float = None
) -> List[Dict[str, Any]]:
    """
    Get relevant context from Vector DB based on query embedding.
    
    This is a convenience function that wraps the query_vectors method
    with additional filtering based on similarity threshold.
    
    Args:
        query_embedding: The query embedding vector
        top_k: Number of results (uses config default if None)
        threshold: Minimum similarity score (uses config default if None)
    
    Returns:
        List of relevant context chunks with metadata
    """
    if top_k is None:
        top_k = settings.top_k_results
    
    if threshold is None:
        threshold = settings.similarity_threshold
    
    results = vector_db.query_vectors(
        query_vector=query_embedding,
        top_k=top_k
    )
    
    # Filter by threshold and extract relevant context
    relevant_contexts = []
    for match in results.get("matches", []):
        if match["score"] >= threshold:
            relevant_contexts.append({
                "text": match["metadata"].get("text", ""),
                "source": match["metadata"].get("source", ""),
                "topic": match["metadata"].get("topic", ""),
                "score": match["score"]
            })
    
    return relevant_contexts
