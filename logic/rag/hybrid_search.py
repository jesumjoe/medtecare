"""
Hybrid Search Engine Orchestrator for Medical Device RAG.
Combines BGE Dense Vector search, BM25 Lexical search, and Cohere/RRF Reranking.
Returns structured historical medical-device evidence.
"""

from typing import List, Dict, Any, Optional
import logging
from logic.rag.embeddings import embeddings_service
from logic.rag.vector_store import vector_store
from logic.rag.bm25 import bm25_retriever
from logic.rag.reranker import reranker_service

logger = logging.getLogger(__name__)

class HybridSearchEngine:
    """Hybrid Search Engine orchestrating dense, lexical, and reranked retrieval."""

    def search(
        self,
        query: str,
        top_k: int = 5,
        use_reranker: bool = True,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Executes Hybrid RAG search across indexed medical device records and knowledge base documents.
        
        Pipeline:
          Query
            │
          ├─► BGE Small Dense Vector Search
          └─► BM25 Lexical Keyword Search
            │
            ▼
          Reciprocal Rank Fusion (RRF) / Optional Cohere Reranker
            │
            ▼
          Structured Medical Device Evidence Records (HISTORICAL_EVIDENCE)
        """
        if not query or not query.strip():
            return []

        # 1. Dense Semantic Retrieval
        query_vector = embeddings_service.embed_text(query)
        dense_results = vector_store.similarity_search(
            query_vector,
            top_k=max(top_k * 2, 10),
            filter_metadata=filter_metadata
        )

        # 2. Lexical Keyword Retrieval
        bm25_results = bm25_retriever.search(
            query,
            top_k=max(top_k * 2, 10),
            filter_metadata=filter_metadata
        )

        # If both are empty, return empty list
        if not dense_results and not bm25_results:
            return []

        # 3. Rerank and Fuse results
        if use_reranker:
            results = reranker_service.rerank(
                query=query,
                dense_results=dense_results,
                bm25_results=bm25_results,
                top_k=top_k,
                use_cohere=True
            )
        else:
            results = reranker_service.reciprocal_rank_fusion(
                dense_results=dense_results,
                bm25_results=bm25_results,
                k=60,
                top_k=top_k
            )

        return results


hybrid_search_engine = HybridSearchEngine()
