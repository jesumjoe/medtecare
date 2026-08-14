"""
Node 3: Knowledge Base RAG Search.
"""

from typing import Dict, Any
from logic.knowledge_base.ingestion import knowledge_ingestion_service
from logic.rag.hybrid_search import hybrid_search_engine

def retrieve_knowledge_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Indexes documents if necessary and executes hybrid search."""
    knowledge_ingestion_service.load_and_index_documents()

    query = f"{state.get('equipment_type', '')} {state.get('predicted_failure', '')} {' '.join(state.get('important_features', []))}"
    docs = hybrid_search_engine.search(query=query, top_k=3)
    
    state["retrieved_documents"] = docs
    state["citations"] = [d.get("title", "OEM Manual") for d in docs]
    return state
