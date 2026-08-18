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
    device_id: Optional[str] = None
    device_name: Optional[str] = None
    equipment_id: str = Field(default="DEV-001", description="Device / Equipment Unique Identifier")
    equipment_type: str = Field(default="Medical Equipment", description="Device Classification or Model Name")
    
    # Squad A CatBoost Specific Fields
    future_event_probability: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="CatBoost predicted probability of future_event")
    prediction: Optional[int] = Field(default=None, description="CatBoost binary prediction class (0 or 1)")
    risk_level: Optional[str] = Field(default=None, description="Risk level category (LOW, MEDIUM, HIGH, CRITICAL)")
    risk_score: float = Field(default=50.0, ge=0.0, le=100.0, description="Risk score scaled 0.0 to 100.0")
    predicted_failure: str = Field(default="medical-device future-event risk", description="Description of predicted future event risk")
    model_confidence: float = Field(default=0.85, ge=0.0, le=1.0, description="Squad A ML model confidence metric 0.0 to 1.0")
    important_features: List[str] = Field(default_factory=list, description="Key features contributing to the risk score")
    feature_drivers: List[Any] = Field(default_factory=list, description="Raw Squad A SHAP feature drivers")
    
    # Medical Device Domain Metadata (Squad A Dataset Columns)
    classification: str = Field(default="Medical Device", description="Device classification category")
    risk_class: str = Field(default="Class II", description="Device regulatory risk class e.g. Class I, Class IIa, Class IIb, Class III")
    manufacturer: str = Field(default="OEM Manufacturer", description="Manufacturer name")
    parent_company: Optional[str] = Field(default="", description="Parent company name")
    country: Optional[str] = Field(default="", description="Country of origin")
    previous_events: int = Field(default=0, ge=0, description="Historical adverse event count")
    previous_recalls: int = Field(default=0, ge=0, description="Historical recall count")
    previous_safety_notices: int = Field(default=0, ge=0, description="Historical safety notice count")
    years_in_service: float = Field(default=0.0, ge=0.0, description="Device operational age in years")
    
    telemetry: List[TelemetryMetric] = Field(default_factory=list, description="Legacy telemetry container (empty for Squad A)")

    def model_post_init(self, __context: Any) -> None:
        """Synchronize alias fields upon initialization."""
        if self.device_id and not self.equipment_id:
            self.equipment_id = self.device_id
        elif self.equipment_id and not self.device_id:
            self.device_id = self.equipment_id

        if self.device_name and self.equipment_type == "Medical Equipment":
            self.equipment_type = self.device_name
        elif self.equipment_type and not self.device_name:
            self.device_name = self.equipment_type

        if self.future_event_probability is not None and self.risk_score == 50.0:
            self.risk_score = self.future_event_probability * 100.0

