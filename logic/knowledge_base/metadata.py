"""
Medical Device & OEM Knowledge Base Metadata Schema.
Preserves official global medical device dataset attributes and historical records.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field

EvidenceType = Literal["HISTORICAL_EVIDENCE", "DOCUMENT_EVIDENCE", "MODEL_EVIDENCE", "AI_INFERENCE"]

class MedicalDeviceMetadata(BaseModel):
    """Structured metadata for medical devices in the RAG knowledge base.
    
    Target Leakage Prevention:
    - `future_event` (Squad A prediction target) is strictly EXCLUDED.
    - All attributes represent historical, verified device history.
    """
    device_id: str = Field(..., description="Unique device identifier (e.g., DEV-001, MD-10492)")
    device_name: str = Field(..., description="Commercial or standard medical device name")
    classification: str = Field(default="General Medical Device", description="FDA / ISO / Global classification")
    risk_class: str = Field(default="Class II", description="Device Risk Class: Class I, Class II, or Class III")
    country: str = Field(default="Global", description="Country of manufacture or deployment")
    manufacturer: str = Field(default="Unknown OEM", description="Medical device manufacturing organization")
    parent_company: Optional[str] = Field(default=None, description="Parent corporate entity")
    previous_events: int = Field(default=0, ge=0, description="Historical adverse incident / malfunction events")
    previous_recalls: int = Field(default=0, ge=0, description="Historical safety recall count")
    previous_safety_notices: int = Field(default=0, ge=0, description="Historical safety alert / warning notices")
    years_in_service: float = Field(default=1.0, ge=0.0, description="Operating lifespan in service")
    title: str = Field(default="", description="Searchable title / label")
    section: str = Field(default="Historical Safety Record", description="Knowledge section or document category")
    evidence_type: EvidenceType = Field(default="HISTORICAL_EVIDENCE", description="Evidence category classification")


class DocumentMetadata(BaseModel):
    """Schema for technical manuals, OEM guidelines, and service bulletins."""
    document_id: str
    title: str
    section: str
    equipment_type: Optional[str] = "medical_device"
    oem_source: Optional[str] = "OEM Maintenance Manual"
    evidence_type: EvidenceType = "DOCUMENT_EVIDENCE"
