"""
BM25 Lexical Keyword Search Retriever for Medical Device Records & Manuals.
Uses rank-bm25 (Okapi BM25) for lexical exact and keyword matching.
"""

from typing import List, Dict, Any, Optional
import re
import logging

logger = logging.getLogger(__name__)

class BM25Retriever:
    """BM25 Lexical Index for Medical Device Records and Guides."""

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.bm25 = None

    def _tokenize(self, text: str) -> List[str]:
        """Tokenizes text into lowercase tokens, handling medical terms and hyphenated IDs."""
        if not text:
            return []
        # Split on non-alphanumeric except hyphen and underscore
        tokens = re.findall(r"[\w\-]+", text.lower())
        # Expand hyphenated terms as both joined and separated tokens
        expanded = []
        for t in tokens:
            expanded.append(t)
            if "-" in t:
                parts = t.split("-")
                expanded.extend([p for p in parts if len(p) > 1])
        return expanded

    def index_documents(self, documents: List[Dict[str, Any]]):
        """Indexes document chunks into BM25 corpus."""
        self.documents = documents
        if not documents:
            self.bm25 = None
            return

        try:
            from rank_bm25 import BM25Okapi
            corpus = [
                self._tokenize(
                    f"{doc.get('content', '')} {doc.get('title', '')} {doc.get('classification', '')} "
                    f"{doc.get('manufacturer', '')} {doc.get('device_id', '')} {doc.get('risk_class', '')}"
                )
                for doc in documents
            ]
            self.bm25 = BM25Okapi(corpus)
        except Exception as e:
            logger.error(f"Error initializing BM25Okapi: {e}")
            self.bm25 = None

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Executes Okapi BM25 keyword search against query with optional metadata filtering."""
        if not self.bm25 or not self.documents or not query.strip():
            return []

        tokenized_query = self._tokenize(query)
        if not tokenized_query:
            return []

        doc_scores = self.bm25.get_scores(tokenized_query)
        
        # Build candidate list with filtering
        scored_docs = []
        for idx, score in enumerate(doc_scores):
            if score <= 0:
                continue
            doc = self.documents[idx]
            if filter_metadata:
                match = all(doc.get(k) == v for k, v in filter_metadata.items())
                if not match:
                    continue
            scored_docs.append((idx, float(score)))

        if not scored_docs:
            return []

        scored_docs.sort(key=lambda x: x[1], reverse=True)
        max_score = max(s for _, s in scored_docs) if scored_docs else 1.0
        if max_score <= 0:
            max_score = 1.0

        results = []
        for idx, score in scored_docs[:top_k]:
            doc_copy = self.documents[idx].copy()
            doc_copy["relevance_score"] = round(min(score / max_score, 1.0), 4)
            doc_copy["retrieval_method"] = "bm25_lexical"
            results.append(doc_copy)

        return results

    def clear(self):
        """Clears indexed documents and BM25 model."""
        self.documents.clear()
        self.bm25 = None

    def __len__(self) -> int:
        return len(self.documents)


bm25_retriever = BM25Retriever()
