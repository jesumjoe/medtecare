"""
Reranker Service: Reciprocal Rank Fusion (RRF) & Optional Cohere API Reranking.
Combines BGE Dense Vector and BM25 Lexical search result sets into a unified,
calibrated ranking of medical device records and OEM documentation.

Cohere Reranker is purely OPTIONAL:
- If COHERE_API_KEY is not configured or fails, RRF operates locally without any paid API keys.
"""

from typing import List, Dict, Any, Optional
import os
import logging

logger = logging.getLogger(__name__)

class RerankerService:
    """Hybrid rank combination and reranking service with RRF and optional Cohere API."""

    def __init__(self):
        self.cohere_client = None
        self._init_cohere()

    def _init_cohere(self):
        """Initializes Cohere client if COHERE_API_KEY is present."""
        cohere_key = os.getenv("COHERE_API_KEY", "").strip()
        if cohere_key:
            try:
                import cohere
                # Support both Cohere v5+ Client and ClientV2
                self.cohere_client = cohere.Client(api_key=cohere_key)
                logger.info("Cohere Reranker client initialized successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize Cohere client: {e}. Defaulting to RRF.")
                self.cohere_client = None
        else:
            self.cohere_client = None

    @property
    def has_cohere(self) -> bool:
        """Returns True if Cohere API client is active and configured."""
        if not self.cohere_client and os.getenv("COHERE_API_KEY", "").strip():
            self._init_cohere()
        return self.cohere_client is not None

    def rerank(
        self,
        query: str,
        dense_results: List[Dict[str, Any]],
        bm25_results: List[Dict[str, Any]],
        top_k: int = 5,
        use_cohere: bool = True
    ) -> List[Dict[str, Any]]:
        """Combines and reranks dense vector and BM25 lexical results using Cohere (if available) or RRF."""
        # 1. Deduplicate candidates by document ID
        candidate_map: Dict[str, Dict[str, Any]] = {}
        for doc in dense_results + bm25_results:
            doc_id = str(doc.get("id") or hash(doc.get("content", "")))
            if doc_id not in candidate_map:
                candidate_map[doc_id] = doc

        candidates = list(candidate_map.values())
        if not candidates:
            return []

        # 2. Try Optional Cohere Reranking if enabled & configured
        if use_cohere and self.has_cohere:
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
                logger.warning(f"Cohere API call failed: {e}. Falling back to Reciprocal Rank Fusion (RRF).")

        # 3. Local Reciprocal Rank Fusion (RRF) Fallback
        return self.reciprocal_rank_fusion(dense_results, bm25_results, k=60, top_k=top_k)

    def reciprocal_rank_fusion(
        self,
        dense_results: List[Dict[str, Any]],
        bm25_results: List[Dict[str, Any]],
        k: int = 60,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Executes Reciprocal Rank Fusion algorithm:
        RRF_Score(d) = sum_{method} ( 1 / (k + rank_method(d)) )
        
        Where:
        - k = 60 (standard IR smoothing parameter)
        - rank is 1-indexed position in retrieval results
        """
        rrf_scores: Dict[str, float] = {}
        doc_store: Dict[str, Dict[str, Any]] = {}

        # Accumulate scores from Dense vector rankings
        for rank, doc in enumerate(dense_results):
            doc_id = str(doc.get("id") or hash(doc.get("content", "")))
            doc_store[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank + 1))

        # Accumulate scores from BM25 lexical rankings
        for rank, doc in enumerate(bm25_results):
            doc_id = str(doc.get("id") or hash(doc.get("content", "")))
            doc_store[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank + 1))

        if not rrf_scores:
            return []

        sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)[:top_k]
        max_rrf = max(rrf_scores.values()) if rrf_scores else 1.0
        if max_rrf <= 0:
            max_rrf = 1.0

        fused_results = []
        for doc_id in sorted_ids:
            doc = doc_store[doc_id].copy()
            doc["relevance_score"] = round(rrf_scores[doc_id] / max_rrf, 4)
            doc["retrieval_method"] = "hybrid_rrf"
            fused_results.append(doc)

        return fused_results


reranker_service = RerankerService()
