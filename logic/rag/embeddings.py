"""
BGE Embeddings Service for Squad B Dense Retrieval.
Loads BAAI/bge-small-en-v1.5 sentence-transformers with a lightweight fallback vectorizer.
"""

from typing import List
import numpy as np
import logging

logger = logging.getLogger(__name__)

class BGEmbeddingsService:
    """BGE Vector Embedding Service."""
    
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.st_model = None
        self._initialized = False
        
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading BGE Embedding model: {model_name}...")
            self.st_model = SentenceTransformer(model_name)
            self._initialized = True
            logger.info("BGE Embedding model loaded successfully.")
        except Exception as e:
            logger.warning(f"SentenceTransformer '{model_name}' fallback active: {e}")
            self._initialized = False

    def embed_text(self, text: str) -> List[float]:
        """Generates a dense vector embedding for a single string."""
        return self.embed_documents([text])[0]

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Generates dense vector embeddings for a list of text strings."""
        if not documents:
            return []
            
        if self._initialized and self.st_model:
            try:
                embeddings = self.st_model.encode(documents, normalize_embeddings=True)
                return embeddings.tolist()
            except Exception as e:
                logger.error(f"Error during SentenceTransformer encoding: {e}")

        # Deterministic 384-dimensional normalized hashing vector fallback
        return [self._fallback_embedding(doc) for doc in documents]

    def _fallback_embedding(self, text: str, dim: int = 384) -> List[float]:
        """Normalized hash embedding fallback."""
        vec = np.zeros(dim, dtype=np.float32)
        words = text.lower().split()
        for i, word in enumerate(words):
            for char in word:
                idx = (ord(char) * 31 + i) % dim
                vec[idx] += 1.0
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

embeddings_service = BGEmbeddingsService()
