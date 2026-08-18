"""
Comprehensive Unit & Integration Test Suite for Medical Device RAG & Knowledge Base.
Tests:
  1. Medical-device ingestion
  2. Metadata preservation
  3. BGE dense vector retrieval
  4. BM25 lexical retrieval
  5. Hybrid retrieval
  6. RRF fallback
  7. Optional Cohere reranking
  8. Medical-device domain queries
  9. Target leakage protection
"""

import pytest
from typing import List, Dict, Any

from logic.knowledge_base.ingestion import KnowledgeBaseIngestion, knowledge_ingestion_service
from logic.knowledge_base.metadata import MedicalDeviceMetadata
from logic.knowledge_base.chunking import format_medical_device_record, chunk_text
from logic.rag.embeddings import BGEmbeddingsService, embeddings_service
from logic.rag.bm25 import BM25Retriever, bm25_retriever
from logic.rag.vector_store import LocalVectorStore, vector_store
from logic.rag.reranker import RerankerService, reranker_service
from logic.rag.hybrid_search import HybridSearchEngine, hybrid_search_engine


# --- Small Isolated Test Fixtures (Do NOT load 118k rows in unit tests!) ---
SAMPLE_MEDICAL_DEVICES = [
    {
        "device_id": "MD-INF-001",
        "device_name": "Alaris Infusion Pump 8100",
        "classification": "Infusion Delivery System",
        "risk_class": "Class II",
        "country": "United States",
        "manufacturer": "CareFusion BD",
        "parent_company": "Becton Dickinson",
        "previous_events": 3,
        "previous_recalls": 1,
        "previous_safety_notices": 2,
        "years_in_service": 3.5,
        "failure_mode": "Downstream occlusion pressure sensor calibration drift",
        "future_event": 1  # TARGET LEAKAGE TEST CANDIDATE (Must NOT leak!)
    },
    {
        "device_id": "MD-DEF-002",
        "device_name": "LifePak 15 Defibrillator Monitor",
        "classification": "Cardiovascular Defibrillator",
        "risk_class": "Class III",
        "country": "Germany",
        "manufacturer": "Physio-Control",
        "parent_company": "Stryker",
        "previous_events": 1,
        "previous_recalls": 0,
        "previous_safety_notices": 1,
        "years_in_service": 2.0,
        "failure_mode": "Capacitor charge cycle delayed beyond 10s threshold",
        "future_event": 0  # TARGET LEAKAGE TEST CANDIDATE
    },
    {
        "device_id": "MD-SURG-003",
        "device_name": "DaVinci Xi Surgical Robot Endowrist",
        "classification": "Robotic Surgical System",
        "risk_class": "Class II",
        "country": "United States",
        "manufacturer": "Intuitive Surgical",
        "parent_company": "Intuitive Surgical",
        "previous_events": 4,
        "previous_recalls": 1,
        "previous_safety_notices": 3,
        "years_in_service": 4.1,
        "failure_mode": "Master tool manipulator joint cable tension slack",
        "future_event": 1  # TARGET LEAKAGE TEST CANDIDATE
    },
    {
        "device_id": "MD-VEN-004",
        "device_name": "Puritan Bennett 980 Ventilator",
        "classification": "Mechanical Ventilator",
        "risk_class": "Class III",
        "country": "Ireland",
        "manufacturer": "Medtronic Covidien",
        "parent_company": "Medtronic",
        "previous_events": 2,
        "previous_recalls": 0,
        "previous_safety_notices": 1,
        "years_in_service": 5.0,
        "failure_mode": "Exhalation flow sensor measurement drift",
        "future_event": 0  # TARGET LEAKAGE TEST CANDIDATE
    }
]


@pytest.fixture(autouse=True)
def setup_isolated_index():
    """Seeds an isolated in-memory knowledge base index before each test."""
    knowledge_ingestion_service.index_medical_device_records(SAMPLE_MEDICAL_DEVICES)
    yield


# 1. Test Ingestion & Document Creation
def test_medical_device_ingestion():
    """Verifies indexing returns correct document count and populates indices."""
    assert len(vector_store) == len(SAMPLE_MEDICAL_DEVICES)
    assert len(bm25_retriever) == len(SAMPLE_MEDICAL_DEVICES)


# 2. Test Metadata Preservation
def test_metadata_preservation():
    """Verifies that all specified medical device metadata fields are preserved in indexed documents."""
    results = bm25_retriever.search("Alaris Infusion Pump", top_k=1)
    assert len(results) > 0
    doc = results[0]
    
    assert doc["device_id"] == "MD-INF-001"
    assert doc["device_name"] == "Alaris Infusion Pump 8100"
    assert doc["classification"] == "Infusion Delivery System"
    assert doc["risk_class"] == "Class II"
    assert doc["country"] == "United States"
    assert doc["manufacturer"] == "CareFusion BD"
    assert doc["parent_company"] == "Becton Dickinson"
    assert doc["previous_events"] == 3
    assert doc["previous_recalls"] == 1
    assert doc["previous_safety_notices"] == 2
    assert doc["years_in_service"] == 3.5
    assert doc["evidence_type"] == "HISTORICAL_EVIDENCE"


# 3. Test Target Leakage Protection
def test_target_leakage_protection():
    """CRITICAL: Verifies `future_event` is NOT present in any indexed document or metadata."""
    for doc in vector_store.documents:
        assert "future_event" not in doc, "Target leakage detected in vector store document dictionary!"
        assert "future_event" not in doc["content"].lower(), "Target leakage detected inside document content string!"

    for doc in bm25_retriever.documents:
        assert "future_event" not in doc, "Target leakage detected in BM25 document dictionary!"


# 4. Test BGE Dense Vector Retrieval
def test_bge_dense_vector_retrieval():
    """Verifies BGE vector embedding similarity search returns relevant medical device matches."""
    query_vec = embeddings_service.embed_text("cardiovascular defibrillator capacitor charging delay")
    results = vector_store.similarity_search(query_vec, top_k=2)

    assert len(results) > 0
    assert "relevance_score" in results[0]
    assert results[0]["retrieval_method"] == "dense_vector"
    assert any("Defibrillator" in doc["device_name"] for doc in results)


# 5. Test BM25 Lexical Keyword Retrieval
def test_bm25_lexical_retrieval():
    """Verifies BM25 exact keyword matching for specific medical device models and manufacturers."""
    results = bm25_retriever.search("DaVinci Endowrist Intuitive Surgical", top_k=2)
    assert len(results) > 0
    assert results[0]["retrieval_method"] == "bm25_lexical"
    assert results[0]["device_id"] == "MD-SURG-003"
    assert results[0]["manufacturer"] == "Intuitive Surgical"


# 6. Test Hybrid Retrieval & RRF Fusion
def test_hybrid_rrf_retrieval():
    """Verifies hybrid search combines BGE and BM25 and scores with Reciprocal Rank Fusion."""
    results = hybrid_search_engine.search(
        query="ventilator exhalation flow sensor drift Medtronic",
        top_k=2,
        use_reranker=False
    )
    assert len(results) > 0
    top = results[0]
    assert top["retrieval_method"] == "hybrid_rrf"
    assert 0.0 <= top["relevance_score"] <= 1.0
    assert "Ventilator" in top["device_name"] or "Medtronic" in top["manufacturer"]


# 7. Test RRF Fallback when Cohere Unavailable
def test_rrf_fallback_without_cohere(monkeypatch):
    """Verifies that when COHERE_API_KEY is absent, system falls back gracefully to RRF."""
    monkeypatch.delenv("COHERE_API_KEY", raising=False)
    fresh_reranker = RerankerService()
    assert fresh_reranker.has_cohere is False

    dense_docs = vector_store.similarity_search(embeddings_service.embed_text("infusion pump"), top_k=2)
    bm25_docs = bm25_retriever.search("infusion pump", top_k=2)
    
    fused = fresh_reranker.rerank("infusion pump", dense_docs, bm25_docs, top_k=2)
    assert len(fused) > 0
    assert fused[0]["retrieval_method"] == "hybrid_rrf"


# 8. Test Optional Cohere Reranking Interface
def test_optional_cohere_reranking():
    """Verifies Cohere reranking interface handles mocking and fallbacks cleanly."""
    dense_docs = vector_store.similarity_search(embeddings_service.embed_text("surgical robot"), top_k=2)
    bm25_docs = bm25_retriever.search("surgical robot", top_k=2)

    # Calling rerank with active service
    results = reranker_service.rerank(
        query="robotic arm joint tension",
        dense_results=dense_docs,
        bm25_results=bm25_docs,
        top_k=2
    )
    assert len(results) > 0
    assert "relevance_score" in results[0]


# 9. Test Domain-Specific Medical Queries
@pytest.mark.parametrize("query,expected_keyword", [
    ("occlusion pressure sensor drift", "Infusion"),
    ("defibrillator high voltage charging", "Defibrillator"),
    ("robotic surgical manipulator cable", "Surgical"),
    ("mechanical ventilator exhalation measurement", "Ventilator"),
])
def test_domain_medical_queries(query, expected_keyword):
    """Verifies domain-specific medical malfunction queries match the right device records."""
    results = hybrid_search_engine.search(query=query, top_k=2)
    assert len(results) > 0
    match = any(expected_keyword.lower() in (d["device_name"] + " " + d["classification"]).lower() for d in results)
    assert match, f"Expected keyword '{expected_keyword}' in results for query: '{query}'"


# 10. Test Metadata Filtering (Risk Class & Classification)
def test_metadata_filtering():
    """Verifies vector search and BM25 can filter by regulatory risk class (e.g., Class III)."""
    results = vector_store.similarity_search(
        embeddings_service.embed_text("medical device"),
        top_k=5,
        filter_metadata={"risk_class": "Class III"}
    )
    assert len(results) > 0
    for doc in results:
        assert doc["risk_class"] == "Class III"
