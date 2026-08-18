"""
Node 1: Validate ML Prediction Input.
"""

from typing import Dict, Any

def validate_prediction_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Validates Squad A ML prediction input or applies medical device fallback values."""
    dev_id = state.get("device_id") or state.get("equipment_id") or "DEV-88401"
    state["device_id"] = dev_id
    state["equipment_id"] = dev_id
    
    dev_name = state.get("device_name") or state.get("equipment_type") or "Infusion Pump System"
    state["device_name"] = dev_name
    state["equipment_type"] = dev_name

    prob = state.get("future_event_probability")
    if prob is not None:
        state["risk_score"] = float(prob) * 100.0 if prob <= 1.0 else float(prob)
        state["model_confidence"] = state.get("model_confidence", prob)
    elif state.get("risk_score") is None:
        state["risk_score"] = 75.0

    if not state.get("predicted_failure") or state.get("predicted_failure") == "Elevated Mechanical Vibration & Thermal Spike":
        state["predicted_failure"] = "medical-device future-event risk"

    if not state.get("model_confidence"):
        state["model_confidence"] = 0.87

    if not state.get("classification"):
        state["classification"] = "Active Infusion Equipment"

    if not state.get("risk_class"):
        state["risk_class"] = "Class IIb"

    return state

