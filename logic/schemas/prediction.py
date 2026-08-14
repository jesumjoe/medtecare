"""
Squad A Input Contract: ML Prediction Schema.
Defines the exact structure expected from Squad A's ML predictive model.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TelemetryMetric(BaseModel):
    name: str
    value: float
    unit: str
    normal_range: Optional[List[float]] = None

class MLPrediction(BaseModel):
    equipment_id: str
    equipment_type: str = "Industrial Motor"
    telemetry: List[TelemetryMetric] = Field(default_factory=list)
    risk_score: float = Field(..., ge=0.0, le=100.0, description="Risk score scaled 0.0 to 100.0 (or 0.0 to 1.0)")
    predicted_failure: str = Field(..., description="Predicted failure type e.g. Bearing Failure, Spindle Overheating")
    model_confidence: float = Field(..., ge=0.0, le=1.0, description="Squad A ML model confidence metric 0.0 to 1.0")
    important_features: List[str] = Field(default_factory=list, description="Key features contributing to the risk score")
