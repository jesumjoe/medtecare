"""
Hybrid Search Engine Orchestrator.
Combines BGE Dense Vector search, BM25 Lexical search, and Cohere/RRF Reranking.
"""

from typing import List, Dict, Any, Optional
from logic.rag.embeddings import embeddings_service
from logic.rag.vector_store import vector_store
from logic.rag.bm25 import bm25_retriever
from logic.rag.reranker import reranker_service

class HybridSearchEngine:
    """Hybrid Search Engine orchestrating dense, lexical, and reranked retrieval."""

    def search(self, query: str, top_k: int = 5, use_reranker: bool = True) -> List[Dict[str, Any]]:
        """Executes Hybrid RAG search query."""
        # 1. Dense retrieval
        query_vector = embeddings_service.embed_text(query)
        dense_results = vector_store.similarity_search(query_vector, top_k=top_k * 2)

        # 2. Lexical retrieval
        bm25_results = bm25_retriever.search(query, top_k=top_k * 2)

        # 3. Reranking
        if use_reranker:
            return reranker_service.rerank(query, dense_results, bm25_results, top_k=top_k)
        
        return dense_results[:top_k]

hybrid_search_engine = HybridSearchEngine()
