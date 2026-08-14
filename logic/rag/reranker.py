"""
Cohere Reranker with Reciprocal Rank Fusion (RRF) Fallback.
Uses Cohere API if COHERE_API_KEY is available, or performs
RRF hybrid rank fusion across BM25 and Dense vector results.
"""

from typing import List, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)

class RerankerService:
    """Reranking service with Cohere API and local RRF fusion fallback."""

    def __init__(self):
        self.cohere_client = None
        cohere_key = os.getenv("COHERE_API_KEY", "")
        if cohere_key:
            try:
                import cohere
                self.cohere_client = cohere.Client(api_key=cohere_key)
                logger.info("Cohere Reranker client initialized successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize Cohere client: {e}")

    def rerank(self, query: str, dense_results: List[Dict[str, Any]], bm25_results: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """Combines and reranks dense vector and BM25 lexical search results."""
        candidate_map: Dict[str, Dict[str, Any]] = {}
        for doc in dense_results + bm25_results:
            doc_id = doc.get("id") or hash(doc["content"])
            if doc_id not in candidate_map:
                candidate_map[doc_id] = doc

        candidates = list(candidate_map.values())
        if not candidates:
            return []

        if self.cohere_client:
            try:
                texts = [doc["content"] for doc in candidates]
                response = self.cohere_client.rerank(
                    model="rerank-english-v3.0",
                    query=query,
                    documents=texts,
                    top_n=min(top_k, len(candidates))
                )
                reranked_results = []
                for result in response.results:
                    doc = candidates[result.index].copy()
                    doc["relevance_score"] = round(float(result.relevance_score), 4)
                    doc["retrieval_method"] = "cohere_reranked"
                    reranked_results.append(doc)
                return reranked_results
            except Exception as e:
                logger.warning(f"Cohere rerank fallback to RRF: {e}")

        return self._reciprocal_rank_fusion(dense_results, bm25_results, top_k=top_k)

    def _reciprocal_rank_fusion(self, dense_results: List[Dict[str, Any]], bm25_results: List[Dict[str, Any]], k: int = 60, top_k: int = 5) -> List[Dict[str, Any]]:
        """Reciprocal Rank Fusion algorithm combining rank lists."""
        rrf_scores: Dict[str, float] = {}
        doc_store: Dict[str, Dict[str, Any]] = {}

        for rank, doc in enumerate(dense_results):
            doc_id = doc.get("id") or hash(doc["content"])
            doc_store[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank + 1))

        for rank, doc in enumerate(bm25_results):
            doc_id = doc.get("id") or hash(doc["content"])
            doc_store[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank + 1))

        sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)[:top_k]
        max_rrf = max(rrf_scores.values()) if rrf_scores else 1.0

        fused_results = []
        for doc_id in sorted_ids:
            doc = doc_store[doc_id].copy()
            doc["relevance_score"] = round(rrf_scores[doc_id] / max_rrf, 4)
            doc["retrieval_method"] = "hybrid_rrf"
            fused_results.append(doc)

        return fused_results

reranker_service = RerankerService()
