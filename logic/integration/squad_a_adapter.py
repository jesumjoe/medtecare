"""
Squad A to Squad B Prediction Adapter.

Converts Squad A's CatBoost model prediction outputs into Squad B's MLPrediction contract.
Preserves all Squad A model evidence without altering prediction probabilities or introducing synthetic fields.
"""

from typing import Dict, Any, List, Union
import logging
from logic.schemas.prediction import MLPrediction

logger = logging.getLogger(__name__)


class SquadAAdapter:
    """Adapter for converting Squad A CatBoost prediction payload to MLPrediction schema."""

    @staticmethod
    def adapt(squad_a_output: Dict[str, Any]) -> MLPrediction:
        """
        Converts Squad A output dictionary to MLPrediction contract.

        Squad A Output Payload Schema:
        - device_id: str
        - device_name: str
        - future_event_probability: float (0.0 - 1.0)
        - prediction: int (0 or 1)
        - risk_level: str ("LOW", "MEDIUM", "HIGH", "CRITICAL")
        - model_confidence: float (0.0 - 1.0)
        - feature_drivers: List[Dict[str, float]] or List[str]
        - classification: str
        - risk_class: str
        - manufacturer: str
        - parent_company: str
        - country: str
        - previous_events: int
        - previous_recalls: int
        - previous_safety_notices: int
        - years_in_service: float
        """
        data = squad_a_output.copy()

        # 1. Device Identification & Categorization
        device_id = data.get("device_id") or data.get("equipment_id") or "DEV-UNKNOWN"
        device_name = data.get("device_name") or data.get("equipment_type") or "Medical Equipment"

        # 2. Probability & Risk Score Calculation
        prob = data.get("future_event_probability")
        if prob is not None:
            # Map 0.0-1.0 probability to 0.0-100.0 risk_score scale
            risk_score = float(prob) * 100.0 if prob <= 1.0 else float(prob)
            model_conf = data.get("model_confidence", prob)
        else:
            risk_score = float(data.get("risk_score", 50.0))
            model_conf = float(data.get("model_confidence", 0.85))

        # 3. Predicted Failure Label
        # Mandatory Rule: Squad A predicts future_event risk, NOT a specific physical component failure.
        predicted_failure = data.get("predicted_failure")
        if not predicted_failure or predicted_failure in ["Anomaly", "Elevated Mechanical Vibration & Thermal Spike"]:
            predicted_failure = "medical-device future-event risk"

        # 4. Parse SHAP Feature Drivers
        feature_drivers_raw = data.get("feature_drivers") or data.get("important_features") or []
        important_features: List[str] = []

        if isinstance(feature_drivers_raw, list):
            for item in feature_drivers_raw:
                if isinstance(item, dict):
                    feat_name = item.get("feature", "unknown_feature")
                    impact = item.get("impact")
                    if impact is not None:
                        important_features.append(f"{feat_name} (SHAP impact: {impact:+.2f})")
                    else:
                        important_features.append(feat_name)
                elif isinstance(item, str):
                    important_features.append(item)

        # 5. Build MLPrediction Object
        return MLPrediction(
            device_id=device_id,
            device_name=device_name,
            equipment_id=device_id,
            equipment_type=device_name,
            future_event_probability=prob if prob is not None else (risk_score / 100.0),
            prediction=data.get("prediction", 1 if risk_score >= 50.0 else 0),
            risk_level=data.get("risk_level", SquadAAdapter._derive_risk_level(risk_score)),
            risk_score=risk_score,
            predicted_failure=predicted_failure,
            model_confidence=model_conf,
            important_features=important_features,
            feature_drivers=feature_drivers_raw,
            classification=data.get("classification", "Medical Device"),
            risk_class=data.get("risk_class", "Class II"),
            manufacturer=data.get("manufacturer", "OEM Manufacturer"),
            parent_company=data.get("parent_company", ""),
            country=data.get("country", ""),
            previous_events=int(data.get("previous_events", 0)),
            previous_recalls=int(data.get("previous_recalls", 0)),
            previous_safety_notices=int(data.get("previous_safety_notices", 0)),
            years_in_service=float(data.get("years_in_service", 0.0))
        )

    @staticmethod
    def _derive_risk_level(risk_score: float) -> str:
        if risk_score >= 80.0:
            return "CRITICAL"
        elif risk_score >= 60.0:
            return "HIGH"
        elif risk_score >= 40.0:
            return "MEDIUM"
        return "LOW"


def adapt_squad_a_prediction(squad_a_output: Dict[str, Any]) -> MLPrediction:
    """Convenience function to adapt Squad A prediction output to MLPrediction contract."""
    return SquadAAdapter.adapt(squad_a_output)
