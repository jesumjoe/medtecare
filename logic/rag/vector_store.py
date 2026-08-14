"""
Local Vector Store Service for Dense Retrieval.
Provides cosine similarity search over embedded document chunks.
Compatible interface for future Qdrant/Pinecone/ChromaDB swapping.
"""

from typing import List, Dict, Any
import numpy as np

class LocalVectorStore:
    """In-memory Vector Storage with Cosine Similarity Search."""

    def __init__(self):
        self.vectors: List[np.ndarray] = []
        self.documents: List[Dict[str, Any]] = []

    def add_documents(self, documents: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Adds document chunks and their corresponding embeddings to vector index."""
        for doc, emb in zip(documents, embeddings):
            self.documents.append(doc)
            self.vectors.append(np.array(emb, dtype=np.float32))

    def similarity_search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Performs cosine similarity search against query vector."""
        if not self.vectors:
            return []

        q_vec = np.array(query_vector, dtype=np.float32)
        q_norm = np.linalg.norm(q_vec)
        if q_norm == 0:
            return []

        scores = []
        for idx, doc_vec in enumerate(self.vectors):
            d_norm = np.linalg.norm(doc_vec)
            if d_norm == 0:
                score = 0.0
            else:
                score = float(np.dot(q_vec, doc_vec) / (q_norm * d_norm))
            scores.append((idx, score))

        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in scores[:top_k]:
            doc = self.documents[idx].copy()
            doc["relevance_score"] = round(score, 4)
            doc["retrieval_method"] = "dense_vector"
            results.append(doc)

        return results

    def clear(self):
        self.vectors.clear()
        self.documents.clear()

vector_store = LocalVectorStore()
