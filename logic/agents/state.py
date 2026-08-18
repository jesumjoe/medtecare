"""
LangGraph Agent State definition.
Maintains typed state dictionary passed across workflow graph nodes.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field
from logic.schemas.diagnostic import MaintenancePriority

class AgentState(BaseModel):
    device_id: str = "DEV-001"
    device_name: str = "Medical Equipment"
    equipment_id: str = "DEV-001"
    equipment_type: str = "Medical Equipment"
    
    future_event_probability: float = 0.0
    prediction: int = 0
    risk_level: str = "MEDIUM"
    risk_score: float = 0.0
    predicted_failure: str = "medical-device future-event risk"
    model_confidence: float = 0.85
    important_features: List[str] = Field(default_factory=list)
    feature_drivers: List[Any] = Field(default_factory=list)

    classification: str = "Medical Device"
    risk_class: str = "Class II"
    manufacturer: str = "OEM Manufacturer"
    parent_company: str = ""
    country: str = ""
    previous_events: int = 0
    previous_recalls: int = 0
    previous_safety_notices: int = 0
    years_in_service: float = 0.0

    telemetry: List[Dict[str, Any]] = Field(default_factory=list)
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

