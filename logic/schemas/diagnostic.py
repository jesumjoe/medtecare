"""
Squad C Output Contract: Diagnostic Result Schema.
Defines the clean Python object output returned by DiagnosticEngine for Squad C API integration.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

MaintenancePriority = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]

class ProbableRootCause(BaseModel):
    cause: str
    likelihood: float = Field(..., ge=0.0, le=1.0)
    description: str

class EvidenceCategory(BaseModel):
    type: Literal["MODEL_EVIDENCE", "DOCUMENT_EVIDENCE", "HISTORICAL_EVIDENCE", "AI_INFERENCE"]
    description: str
    source: str
    confidence: float

class RecommendedAction(BaseModel):
    step: int
    title: str
    description: str
    timeframe: str
    urgency: MaintenancePriority

class DiagnosticResult(BaseModel):
    equipment_id: str
    equipment_type: str
    risk_score: float
    predicted_failure: str
    diagnosis: str
    probable_root_causes: List[ProbableRootCause] = Field(default_factory=list)
    evidence: List[EvidenceCategory] = Field(default_factory=list)
    historical_context: List[Dict[str, Any]] = Field(default_factory=list)
    explanation: str
    recommended_actions: List[RecommendedAction] = Field(default_factory=list)
    maintenance_priority: MaintenancePriority
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall Squad B agent confidence")
    citations: List[str] = Field(default_factory=list)
    requires_human_review: bool = True
    errors: List[str] = Field(default_factory=list)
