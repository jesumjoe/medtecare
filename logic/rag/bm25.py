"""
BM25 Lexical Search Retriever.
Uses Okapi BM25 for keyword-based maintenance manual search.
"""

from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
import re

class BM25Retriever:
    """BM25 Lexical Index for Knowledge Documents."""

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.bm25: BM25Okapi = None

    def _tokenize(self, text: str) -> List[str]:
        """Tokenizes text into lowercase words."""
        return re.findall(r"\w+", text.lower())

    def index_documents(self, documents: List[Dict[str, Any]]):
        """Indexes document chunks into BM25 corpus."""
        self.documents = documents
        corpus = [self._tokenize(doc["content"] + " " + doc.get("title", "")) for doc in documents]
        if corpus:
            self.bm25 = BM25Okapi(corpus)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Executes BM25 keyword search against query."""
        if not self.bm25 or not self.documents:
            return []

        tokenized_query = self._tokenize(query)
        if not tokenized_query:
            return []

        doc_scores = self.bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_k]

        max_score = max(doc_scores) if doc_scores.size > 0 and max(doc_scores) > 0 else 1.0

        results = []
        for idx in top_indices:
            score = float(doc_scores[idx])
            if score <= 0:
                continue
            doc = self.documents[idx].copy()
            doc["relevance_score"] = round(min(score / max_score, 1.0), 4)
            doc["retrieval_method"] = "bm25_lexical"
            results.append(doc)

        return results

bm25_retriever = BM25Retriever()
