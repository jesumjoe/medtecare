"""
LangGraph Agent State definition.
Maintains typed state dictionary passed across workflow graph nodes.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field
from logic.schemas.diagnostic import MaintenancePriority

class AgentState(BaseModel):
    equipment_id: str
    equipment_type: str = "Industrial Motor"
    telemetry: List[Dict[str, Any]] = Field(default_factory=list)
    risk_score: float = 0.0
    predicted_failure: str = ""
    model_confidence: float = 0.0
    important_features: List[str] = Field(default_factory=list)
    retrieved_documents: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    historical_context: List[Dict[str, Any]] = Field(default_factory=list)
    diagnostic_findings: str = ""
    probable_root_causes: List[Dict[str, Any]] = Field(default_factory=list)
    explanation: str = ""
    recommended_actions: List[Dict[str, Any]] = Field(default_factory=list)
    maintenance_priority: MaintenancePriority = "MEDIUM"
    agent_confidence: float = 0.0
    citations: List[str] = Field(default_factory=list)
    requires_human_review: bool = True
    errors: List[str] = Field(default_factory=list)
