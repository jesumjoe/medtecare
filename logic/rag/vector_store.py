"""
Local Vector Store Service for Dense Vector Retrieval.
Provides cosine similarity search over embedded medical device records and OEM documentation.
"""

from typing import List, Dict, Any, Optional
import numpy as np

class LocalVectorStore:
    """In-memory Vector Store with Cosine Similarity Search."""

    def __init__(self):
        self.vectors: List[np.ndarray] = []
        self.documents: List[Dict[str, Any]] = []

    def add_documents(self, documents: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Adds document chunks and corresponding dense vector embeddings."""
        for doc, emb in zip(documents, embeddings):
            self.documents.append(doc)
            self.vectors.append(np.array(emb, dtype=np.float32))

    def similarity_search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Performs cosine similarity search against query vector with optional metadata filtering."""
        if not self.vectors or not self.documents:
            return []

        q_vec = np.array(query_vector, dtype=np.float32)
        q_norm = np.linalg.norm(q_vec)
        if q_norm == 0:
            return []

        scores = []
        for idx, doc_vec in enumerate(self.vectors):
            doc = self.documents[idx]

            # Optional metadata filtering
            if filter_metadata:
                match = all(doc.get(k) == v for k, v in filter_metadata.items())
                if not match:
                    continue

            d_norm = np.linalg.norm(doc_vec)
            if d_norm == 0:
                score = 0.0
            else:
                score = float(np.dot(q_vec, doc_vec) / (q_norm * d_norm))
            scores.append((idx, score))

        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in scores[:top_k]:
            doc_copy = self.documents[idx].copy()
            doc_copy["relevance_score"] = round(float(score), 4)
            doc_copy["retrieval_method"] = "dense_vector"
            results.append(doc_copy)

        return results

    def clear(self):
        """Clears all vectors and indexed documents."""
        self.vectors.clear()
        self.documents.clear()

    def __len__(self) -> int:
        return len(self.documents)


vector_store = LocalVectorStore()
