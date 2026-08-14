"""
Document Metadata Schema.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel

class DocumentMetadata(BaseModel):
    document_id: str
    title: str
    section: str
    equipment_type: Optional[str] = "general"
    oem_source: Optional[str] = "DEMO OEM Manual"
