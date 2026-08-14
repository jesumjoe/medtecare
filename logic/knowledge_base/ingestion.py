"""
Knowledge Base Document Ingestion Manager.
Loads, chunks, and indexes maintenance manuals into BM25 Lexical & BGE Dense Vector indices.
"""

import os
from typing import List, Dict, Any
import logging
from logic.rag.embeddings import embeddings_service
from logic.rag.vector_store import vector_store
from logic.rag.bm25 import bm25_retriever
from logic.knowledge_base.chunking import chunk_text

logger = logging.getLogger(__name__)

class KnowledgeBaseIngestion:
    """Ingestion service for indexing OEM manuals and guides."""

    def __init__(self, docs_dir: str = "logic/knowledge_base/documents"):
        self.docs_dir = docs_dir
        self._is_indexed = False

    def load_and_index_documents(self) -> int:
        """Loads text files from documents directory and indexes them into RAG pipeline."""
        if self._is_indexed:
            return len(bm25_retriever.documents)

        documents: List[Dict[str, Any]] = []

        if os.path.exists(self.docs_dir):
            for filename in os.listdir(self.docs_dir):
                if filename.endswith(".txt"):
                    filepath = os.path.join(self.docs_dir, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Extract title / section header if present
                    lines = [line.strip() for line in content.splitlines() if line.strip()]
                    title = lines[1].replace("Title: ", "") if len(lines) > 1 and "Title:" in lines[1] else filename
                    section = lines[2].replace("Section: ", "") if len(lines) > 2 and "Section:" in lines[2] else "General"

                    chunks = chunk_text(content, chunk_size=400, chunk_overlap=50)
                    for idx, chunk in enumerate(chunks):
                        documents.append({
                            "id": f"{filename}_{idx}",
                            "title": title,
                            "section": section,
                            "content": chunk,
                            "filename": filename
                        })

        if not documents:
            logger.warning("No documents found in directory. Using fallback demo documents.")
            documents = [
                {
                    "id": "DEMO-001",
                    "title": "SKF Bearing Maintenance Guide",
                    "section": "Chapter 7: Spindle Wear",
                    "content": "[DEMO OEM MANUAL] Spindle bearing temp > 85°C indicates lubricant breakdown. Vibration RMS > 4.5 mm/s requires bearing replacement (SKF 7208 BECBP)."
                }
            ]

        # Generate BGE vector embeddings
        texts = [doc["content"] for doc in documents]
        embeddings = embeddings_service.embed_documents(texts)

        # Populate indices
        vector_store.clear()
        vector_store.add_documents(documents, embeddings)
        bm25_retriever.index_documents(documents)

        self._is_indexed = True
        logger.info(f"Indexed {len(documents)} document chunks into RAG pipeline.")
        return len(documents)

knowledge_ingestion_service = KnowledgeBaseIngestion()
