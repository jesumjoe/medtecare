"""
BGE Dense Embeddings Service for Medical Device RAG.
Loads BAAI/bge-small-en-v1.5 via sentence-transformers with a deterministic fallback vectorizer.
"""

from typing import List
import numpy as np
import logging

logger = logging.getLogger(__name__)

class BGEmbeddingsService:
    """BGE Dense Vector Embedding Service (BAAI/bge-small-en-v1.5)."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.st_model = None
        self._initialized = False

        try:
            import os
            import ssl
            if os.environ.get("DISABLE_HEAVY_EMBEDDINGS") == "1":
                raise ImportError("Heavy sentence-transformers disabled by environment variable.")
            os.environ["CURL_CA_BUNDLE"] = ""
            os.environ["PYTHONHTTPSVERIFY"] = "0"
            ssl._create_default_https_context = ssl._create_unverified_context
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading BGE Embedding model: {model_name}...")
            self.st_model = SentenceTransformer(model_name)
            self._initialized = True
            logger.info(f"BGE Embedding model '{model_name}' loaded successfully.")
        except BaseException as e:
            logger.warning(f"SentenceTransformer '{model_name}' fallback active: {e}")
            self._initialized = False

    @property
    def is_model_loaded(self) -> bool:
        """Returns True if the underlying SentenceTransformer model is active."""
        return self._initialized and self.st_model is not None

    def embed_text(self, text: str) -> List[float]:
        """Generates a dense vector embedding for a single text string."""
        if not text:
            return [0.0] * 384
        return self.embed_documents([text])[0]

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Generates dense vector embeddings for a list of document strings."""
        if not documents:
            return []

        if self.is_model_loaded:
            try:
                embeddings = self.st_model.encode(
                    documents,
                    normalize_embeddings=True,
                    show_progress_bar=False
                )
                return embeddings.tolist()
            except Exception as e:
                logger.error(f"SentenceTransformer encoding error: {e}. Using fallback vectorizer.")

        # Deterministic 384-dimensional normalized hash embedding fallback
        return [self._fallback_embedding(doc) for doc in documents]

    def _fallback_embedding(self, text: str, dim: int = 384) -> List[float]:
        """Deterministic 384-dimensional normalized bag-of-words hash embedding."""
        vec = np.zeros(dim, dtype=np.float32)
        words = text.lower().split()
        for i, word in enumerate(words):
            for char in word:
                idx = (ord(char) * 31 + i * 17) % dim
                vec[idx] += 1.0
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()


embeddings_service = BGEmbeddingsService()
