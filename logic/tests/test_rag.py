import pytest
from logic.knowledge_base.ingestion import knowledge_ingestion_service
from logic.rag.hybrid_search import hybrid_search_engine
from logic.rag.bm25 import bm25_retriever
from logic.rag.vector_store import vector_store

def test_knowledge_ingestion():
    num_chunks = knowledge_ingestion_service.load_and_index_documents()
    assert num_chunks > 0

def test_hybrid_search():
    knowledge_ingestion_service.load_and_index_documents()
    results = hybrid_search_engine.search(query="spindle bearing temperature", top_k=3)
    assert len(results) > 0
    assert "content" in results[0]
    assert "relevance_score" in results[0]

def test_bm25_search():
    knowledge_ingestion_service.load_and_index_documents()
    results = bm25_retriever.search("viscosity press", top_k=2)
    assert isinstance(results, list)
