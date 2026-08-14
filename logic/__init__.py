"""
Squad B — The Logic Engine
AI Agents + Knowledge Base + RAG + Text-to-SQL + LLM Diagnostic Reasoning
"""

from logic.schemas.prediction import MLPrediction, TelemetryMetric
from logic.schemas.diagnostic import DiagnosticResult, ProbableRootCause, EvidenceCategory, RecommendedAction
from logic.agents.graph import DiagnosticEngine

__version__ = "1.0.0"
__all__ = [
    "MLPrediction",
    "TelemetryMetric",
    "DiagnosticResult",
    "ProbableRootCause",
    "EvidenceCategory",
    "RecommendedAction",
    "DiagnosticEngine"
]
